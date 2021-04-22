import os
import random
import shutil
from plantcv.plantcv import fatal_error


def sample_images(source_path, dest_path, num=100):
    if not os.path.exists(source_path):
        raise IOError(f"Directory does not exist: {source_path}")

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)  # exist_ok argument does not exist in python 2

    img_element_array = []
    img_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif']

    # If SnapshotInfo exists then need to make a new csv for the random image sample
    if os.path.exists(os.path.join(source_path, 'SnapshotInfo.csv')):

        line_array = []
        input_csv = open(os.path.join(source_path, 'SnapshotInfo.csv'))
        header = input_csv.readline()
        for line in input_csv:
            line = line.rstrip("\n")
            element_arr = line.split(',')
            if element_arr[-1]:
                line_array.append(element_arr)
        input_csv.close()

        # Check to make sure number of imgs to select is less than number of images found
        if num > len(line_array):
            fatal_error(f"Number of images found ({len(line_array)}) less than 'num'.")

        # Create SnapshotInfo file
        out_file = open(os.path.join(dest_path, 'SnapshotInfo.csv'), 'w')
        out_file.write(header)

        # Get random snapshots
        random_index = random.sample(range(0, len(line_array) - 1), num)
        for i in random_index:
            row = line_array[int(i)]
            out_file.write(','.join(row))
            snap_path = os.path.join(source_path, "snapshot" + row[1])
            folder_path = os.path.join(dest_path, "snapshot" + row[1])
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)  # the beginning of folder_path (dest_path) already exists from above
            for root, dirs, files in os.walk(snap_path):
                for file in files:
                    shutil.copy(os.path.join(root, file), folder_path)
    else:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                # Check file type so that only images get copied over
                name, ext = os.path.splitext(file)
                if ext.lower() in img_extensions:
                    img_element_array.append(os.path.join(root, file))

        # Check to make sure number of imgs to select is less than number of images found
        if num > len(img_element_array):
            fatal_error(f"Number of images found ({len(img_element_array)}) less than 'num'.")

        # Get random images
        random_index = random.sample(range(0, len(img_element_array) - 1), num)
        # Copy images over to destination
        for i in random_index:
            shutil.copy(img_element_array[int(i)], dest_path)
