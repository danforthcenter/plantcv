import os
import sys
import random
import shutil

def fill_array_from_csv(filename, name_param):
    line_array = []
    input_file = open(filename, 'r')
    header = input_file.readline()
    for line in input_file:
        if name_param in line:
            element_arr = line.split(',')
            line_array.append(element_arr)
    input_file.close()
    return header, line_array

def copytree_for_real(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    for root, dirs, files in os.walk(source_path):
        for file in files:
            shutil.copy(os.path.join(root, file), dest_path)

def main():
    input_dir  = sys.argv[1]
    output_dir  = sys.argv[2]
    output_csv  = sys.argv[3]
    num_samples = int(sys.argv[4])

    # find input csv
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if ".csv" in file:
                input_csv = file

    # fill line array (an array of arrays) with arrays of each row's contents
    header, line_array = fill_array_from_csv(os.path.join(input_dir, input_csv), "VIS")

    # get random elements
    sample_array = []  # array of sampled elements
    num_arr = []  # keeps track of elements already sampled
    for i in range(0, num_samples):
        r = random.randint(0, len(line_array) - 1)
        while r in num_arr:
            r = random.randint(0, len(line_array) - 1)
        sample_array.append(line_array[r])
        num_arr.append(r)

    # move snapshot folders into output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    out_file = open(os.path.join(output_dir, output_csv), 'w')
    out_file.write(header)
    for element in sample_array:
        out_file.write(','.join(element))
        snap_path = os.path.join(input_dir, "snapshot" + element[1])
        dest_path = os.path.join(output_dir, "snapshot" + element[1])
        copytree_for_real(snap_path, dest_path)

    out_file.close()
if __name__ == "__main__":
    main()