#
# image_processing.py
#
# Written by Junsik Hwang
#

"""Resizes and pads images.

1. pad_square() - if the given image is not square-shaped,
                  add black padding

2. resize_img() - resize the given image with designated size parameters

"""

import argparse
import glob

def read_images_from_input_path(given_input_path):
    """ This function returns image paths in the input directory """
    nested_tmp = [glob.glob("./" + given_input_path + "/" + e) for e in ['*.jpg', '*.png']]
    files = [f for f_ in nested_tmp for f in f_]
    return files


def main():
    """ This function runs other functions when ran as a script """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="type in the input image directory path", type=str)
    parser.add_argument("-o", "--output", help="type in the output image directory path", type=str)
    args = parser.parse_args()
    # print(args)

    input_files = read_images_from_input_path(args.input)
    print(input_files)

if __name__ == '__main__':
    print(main.__doc__)
    main()
