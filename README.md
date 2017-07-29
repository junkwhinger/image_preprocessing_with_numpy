# image_preprocessing_with_numpy

<hr>

This simple python code adds padding and resizes images.

## Usage

Run `image_processing.py` with the following parameters

* --i: (str) input image directory path
* --o: (str) output image directory path
* --s: (bool) True if you want to make it square-shaped
* --r: (str) output image size (i.e. 28x28)
* --p: (str) prefix for new images

### example
`python3 image_processing.py --i img --o output_path --s True --r 128x128 --p n`
