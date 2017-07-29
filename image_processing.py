#
# image_processing.py
#
# Written by Junsik Hwang
#

"""Resizes and pads images.

Reference
---------
https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
"""
import argparse
import glob
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imresize
from tqdm import tqdm


def str2bool(input_str):
    """ this function parses string to boolean for argparse parameters """
    if input_str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif input_str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected')


def read_images_from_input_path(given_input_path):
    """ This function returns image paths in the input directory """
    nested_tmp = [glob.glob("./" + given_input_path + "/" + e) for e in ['*.jpg', '*.png']]
    files = [f for f_ in nested_tmp for f in f_]

    if len(files) < 1:
        raise IOError("There are no image files to process: {}".format(given_input_path))

    return files

def is_square(img_arr):
    """ This function tells if the given image is square-shaped """
    return img_arr.shape[0] == img_arr.shape[1]


def pad_image(img_arr):
    """ This function adds padding to the given image """
    width, height, channel = img_arr.shape[0], img_arr.shape[1], img_arr.shape[2]
    diff = np.abs(width - height)

    if width < height:
        tmp = np.arange(diff * height * channel)
        padding_reshaped = tmp.reshape((diff, height, channel))
        zero_padding = np.zeros_like(padding_reshaped)
        spl = int(diff / 2)
        top_padding = zero_padding[:spl]
        bottom_padding = zero_padding[spl:]
        padded_image = np.concatenate([top_padding, img_arr, bottom_padding])
        return padded_image

    elif width > height:
        tmp = np.arange(diff * width * channel)
        padding_reshaped = tmp.reshape((width, diff, channel))
        zero_padding = np.zeros_like(padding_reshaped)
        spl = int(diff / 2)
        left_padding = zero_padding[:, :spl]
        right_padding = zero_padding[:, spl:]
        padded_image = np.concatenate([left_padding, img_arr, right_padding], axis=1)
        return padded_image


def process_image(img_path, funcs):
    """ This function loads image and apply functions """
    img_arr = plt.imread(img_path)

    if funcs["square"] is True:
        if is_square(img_arr) is False:
            img_arr = pad_image(img_arr)

    if funcs["resize"] is None:
        return img_arr
    else:
        try:
            requested_size = funcs["resize"].split("x")
            width, height = int(requested_size[0]), int(requested_size[1])
        except IndexError:
            print("Invalid size type. Please provide input like 32x32")
        img_arr = imresize(img_arr, (width, height))

    return img_arr

def save_image(img_arr, img_path, given_output_path, given_prefix):
    """ This function saves images into the output path """
    new_given_output_path = "./" + given_output_path
    if not os.path.exists(new_given_output_path):
        os.makedirs(new_given_output_path)

    new_filename = given_prefix + "_" + img_path.split("/")[-1]
    new_path = new_given_output_path + "/" + new_filename

    plt.imsave(fname=new_path, arr=img_arr)


def main():
    """ This function runs other functions when ran as a script """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="type in the input image directory path", type=str)
    parser.add_argument("-o", "--output",
                        help="type in the output image directory path", type=str)
    parser.add_argument("-s", "--square",
                        help="True if images to be square", type=str2bool)
    parser.add_argument("-r", "--resize",
                        help="type in the new size (i.e. 32x32)", type=str)
    parser.add_argument("-p", "--prefix",
                        help="type in the prefix for the new images", type=str, default="n")
    args = parser.parse_args()

    ## get image paths
    input_paths = read_images_from_input_path(args.input)

    funcs_to_run = defaultdict()
    funcs_to_run['square'] = args.square
    funcs_to_run['resize'] = args.resize

    for i in tqdm(range(len(input_paths))):
        ## process image
        processed = process_image(input_paths[i], funcs_to_run)
        ## save new image
        save_image(processed, input_paths[i], args.output, args.prefix)


if __name__ == '__main__':
    main()
