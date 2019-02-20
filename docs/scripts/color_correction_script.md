In the terminal:

```
./pipelinename.py -i testimg.png -o ./output-images -r results.txt -w -D 'print'
```
*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

Python script: 
```python

from plantcv import plantcv as pcv
import cv2
import numpy as np

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the pipeline.

### Main pipeline
def main():
    # Get options
    args = options()

    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    pcv.params.debug = "print" #set debug mode
    
    target_img = cv2.imread("target_img.png")
    source_img = cv2.imread("source1_img.png")
    mask = cv2.imread("test_mask.png", -1) # mask must be read in "as-is" include -1
    #Since target_img and source_img have the same zoom and colorchecker position, the same mask can be used for both.
    
    #.npz files containing target_matrix, source_matrix, and transformation_matrix will be saved to the output_directory file path
    
    output_directory = "./test1"
    
    target_matrix, source_matrix, transformation_matrix, corrected_img = pcv.transform.correct_color(target_img, mask, source_img, mask, output_directory)
    
    transformation_matrix = pcv.transform.load_matrix("./test1/transformation_matrix.npz") #load in transformation_matrix
    
    new_source = cv2.imread("VIS_SV_0_z1_h1_g0_e65_v500_376217_0.png") #read in new image for transformation
    
    #apply transformation
    corrected_img = pcv.transform.apply_transformation_matrix(source_img= new_source, target_img= target_img, transformation_matrix= transformation_matrix)
    
    target_img = cv2.imread("target_img.png")
    source_img = cv2.imread("source_img.png")
    mask = cv2.imread("mask.png", -1) # mask must be read in "as-is" include -1
    #Since target_img and source_img have the same zoom and colorchecker position, the same mask can be used for both. 
    
    # get color matrix of target and save
    target_headers, target_matrix = pcv.transform.get_color_matrix(target_img, mask)
    pcv.transform.save_matrix(target_matrix, "target.npz")
    
    #get color_matrix of source
    source_headers, source_matrix = pcv.transform.get_color_matrix(source_img, mask)
    
    # matrix_a is a matrix of average rgb values for each color ship in source_img, matrix_m is a moore-penrose inverse matrix,
    # matrix_b is a matrix of average rgb values for each color ship in source_img
    
    matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(target_matrix= target_matrix, source_matrix= source_matrix)
    
    # deviance is the measure of how greatly the source image deviates from the target image's color space. 
    # Two images of the same color space should have a deviance of ~0.
    # transformation_matrix is a 9x9 matrix of transformation coefficients 
    
    deviance, transformation_matrix = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b)
    
    corrected_img = pcv.transform.apply_transformation_matrix(source_img= source_img, target_img= target_img, transformation_matrix= transformation_matrix)
    
    """
    
    This program illustrates how to create a gray-scale mask for use with plantcv.transform.correct_color.
    
    """
    from plantcv import plantcv as pcv
    import cv2
    import numpy as np
    
    pcv.params.debug = "plot"
    
    img = cv2.imread("target_img.png") #read in img
    pcv.plot_image(img)
    
    #Using the pixel coordinate on the plotted image, designate a region of interest for an n x n pixel region in each color chip.
    
    dimensions = [50,50]  #pixel ROI dimensions
    
    chips = []
    #Declare first row:
    chips.append(pcv.roi.rectangle(img=img, x=1020, y = 1010, w = dimensions[0], h = dimensions[1])) #white
    chips.append(pcv.roi.rectangle(img=img, x= 1150 , y= 1010 , w = dimensions[0], h = dimensions[1]))#blue
    chips.append(pcv.roi.rectangle(img=img, x= 1280 , y= 1010 , w = dimensions[0], h = dimensions[1]))#orange
    chips.append(pcv.roi.rectangle(img=img, x= 1420 , y= 1010 , w = dimensions[0], h = dimensions[1]))#brown
    
    #declare y_shift
    y_shift = 135
    
    #declare number of total rows
    row_total = 6
    
    #declare all other rows
    for i in range(1, row_total):
    chips.append(pcv.roi.rectangle(img=img, x=1020, y = 1010 + i*(y_shift), w = dimensions[0], h = dimensions[1]))
    chips.append(pcv.roi.rectangle(img=img, x= 1150 , y= 1010 + i*(y_shift), w = dimensions[0], h = dimensions[1]))
    chips.append(pcv.roi.rectangle(img=img, x= 1280 , y= 1010 + i*(y_shift), w = dimensions[0], h = dimensions[1]))
    chips.append(pcv.roi.rectangle(img=img, x= 1420 , y= 1010 + i*(y_shift), w = dimensions[0], h = dimensions[1]))
    
    #remove black and white
    del chips[0]
    del chips[19]
    
    mask = np.zeros(shape=np.shape(img)[:2], dtype = np.uint8()) # create empty mask img.
    
    print mask
    
    # draw contours for each region of interest and give them unique color values.
    
    i=1
    for chip in chips:
    print(chip)
    mask = cv2.drawContours(mask, chip[0], -1, (i*10), -1)
    i+=1
    
    
    pcv.plot_image(mask, cmap="gray")
    
    mask = mask*10  #multiply values in the mask for greater contrast. Exclude if designating have more than 25 color chips.
    
    np.unique(mask)
    
    cv2.imwrite("test_mask.png", mask) #write to file.
    
    from plantcv import plantcv as pcv
    import cv2
    import numpy as np
    import matplotlib
    
    target_img = cv2.imread("target_img.png")
    source_img = cv2.imread("source2_img.png")
    target_mask = cv2.imread("test_mask.png", -1) # mask must be read in "as-is" include -1
    source_mask = cv2.imread("mask2_img.png", -1) 
    
    #.npz files containing target_matrix, source_matrix, and transformation_matrix will be saved to the output_directory file path
    output_directory = "./test1"
    
    target_matrix, source_matrix, transformation_matrix, corrected_img = pcv.transform.correct_color(target_img, target_mask, source_img, source_mask, output_directory)
    
    transformation_matrix = pcv.transform.load_matrix("./test1/transformation_matrix.npz") #load in transformation_matrix
    
    new_source = cv2.imread("VIS_SV_0_z1_h1_g0_e65_v500_376217_0.png") #read in new image for transformation
    
    corrected_img = pcv.transform.apply_transformation_matrix(source_img= new_source, target_img= target_img, transformation_matrix= transformation_matrix) #apply transformation

if __name__ == '__main__':
    main()
```
