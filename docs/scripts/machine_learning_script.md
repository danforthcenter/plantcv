
```
# First, use `plantcv-train.py` to use the training images to output probability density 
# functions (PDFs) for plant and background.

# plantcv-train.py naive_bayes --imgdir ./images --maskdir ./masks --outfile naive_bayes_pdfs.txt --plots
```

The output file from `plantcv-train.py` will contain one row for each color channel (hue, saturation, and value) for
each class (e.g. plant and background). The first and second column are the class and channel label, respectively. The
remaining 256 columns contain the p-value from the PDFs for each intensity value observable in an 8-bit image (0-255).

Once we have the `plantcv-train.py` output file, we can classify pixels in a color image in PlantCV.

```python
#!/usr/bin/env python

import argparse
from plantcv import plantcv as pcv

# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-r2", "--coresult", help="result file.", required=False)
    parser.add_argument("-p", "--pdfs", help="Naive Bayes PDF file.", required=True)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    args = parser.parse_args()
    return args


def main():
    # Get options
    args = options()
    
    # Initialize device counter
    pcv.params.debug = args.debug
    
    # Read in the input image
    vis, path, filename = pcv.readimage(filename=args.image)
    
    # Classify each pixel as plant or background (background and system components)
    masks = pcv.naive_bayes_classifier(rgb_img=vis, pdf_file=args.pdfs)
    
    # Additional steps in the pipeline go here
    
# Call program
if __name__ == '__main__':
    main()
```

*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

Then run `plantcv-pipeline.py` with options set based on the input images, but where the naive Bayes PDF file is input
using the `--other_args` flag, for example:

```bash
plantcv-pipeline.py \
--dir ./my-images \
--pipeline my-naive-bayes-script.py \
--db my-db.sqlite3 \
--outdir . \
--meta imgtype_camera_timestamp \
--create \
--other_args="--pdfs naive_bayes_pdfs.txt"
```
