import ast
#from Interface import *
import PIL.Image


def run_length_encode(image):
   """Encodes image object.

   Args:
       image: an image object of type `PIL.Image`.

   Returns:
       runs: a list of runs of pixels. Each run is a tuple of (color, length).
       size: `PIL.Image.size`, will be used for decoding.
   """

   if image.mode != 'RGB':
       raise ValueError(f'Image mode expected "RGB", but received "{image.mode}".')

   # List of runs to be returned
   runs = []

   # Initialize a run before iterating over image pixels
   # Immediately after entering the loop, (None, None) will be inserted into `runs`
   run = {'color': None, 'length': None}

   for color in image.getdata():
       if color != run['color']:
           # Record the current run
           runs.append((run['color'], run['length']))
           # Construct a new run
           run['color'] = color
           run['length'] = 1
       else:
           run['length'] += 1

   # The last run was not recorded in the loop
   runs.append((run['color'], run['length']))

   # Remove the initialized (None, None) run
   runs.pop(0)

   return runs, image.size


def run_length_decode(runs, size):
    """Decode runs of pixels.

    Args:
        runs: a list of runs of pixels. Each run is a tuple of (color, length).
        size: `PIL.Image.size`, will be used for decoding.

    Returns:
        image: an image object of type `PIL.Image`.
    """

    pixels = []
    for color, length in runs:
        pixels.extend(color for _ in range(length))

    image = PIL.Image.new('RGB', size)
    image.putdata(pixels)

    return image


def read_runs(filepath):
    """Reads runs from text file."""
    with open(filepath) as file:
        size = ast.literal_eval(file.readline())
        runs = [ast.literal_eval(line) for line in file if line]
        return runs, size


def write_runs(filepath, runs, size):
    """Writes runs to text file."""
    with open(filepath, 'w') as file:
        file.write(f'{size}\n')
        for run in runs:
            file.write(f'{run}\n')


def estimate_compression_ratio(image, runs):
    """Estimates the compression ratio after encoding.

    The size of the text file containing the encoding result is large when
    comparing with that of the already compressed image. This function
    estimates the number of bytes in memory needed to store the image and the
    runs then calculate the compression ratio.

    Args:
        image: an image object of type `PIL.Image`.
        runs: result of encoding the `image`.
    """

    # Each of the 3 channels "RGB" occupies 1 byte
    # Each pixel occupies 3 bytes in total
    image_size = image.width * image.height * 3

    print(f'Image size: {image.size}')
    print(f'Image estimated size in bytes: {image.width} × {image.height} × 3 = {image_size}')
    print()

    # Each run has color value ("RGB") and length
    # Color occupies 3 bytes as described above
    # Length occupies 3 bytes since 2 bytes only represent 65536 runs at most
    # Each run occupies 6 bytes in total
    runs_size = len(runs) * 6

    print(f'Number of runs: {len(runs)}')
    print(f'Runs estimated size in bytes: {len(runs)} × 6 = {runs_size}')
    print()

    compression_ratio = image_size / runs_size

    print(f'Estimated compression ratio: {image_size} ÷ {runs_size} = {compression_ratio:.2f}')


def main(image_file, encode_file, decode_file):
    # Read file as `PIL.Image` object
    image = PIL.Image.open(image_file)

    # Encode image object and estimate compression ratio
    runs, size = run_length_encode(image)
    estimate_compression_ratio(image, runs)

    # Write encode info into file
    write_runs(encode_file, runs, size)

    # Read encode info from file
    new_runs, new_size = read_runs(encode_file)

    # Decode runs to retrive `PIL.Image` object
    new_image = run_length_decode(new_runs, new_size)

    # Write image object into file
    new_image.save(decode_file)


if __name__ == 'RLEmain':
    # image_file = 'img.jpg'
    # encode_file = 'lenna_encode.txt'
    # decode_file = 'lenna_decode.png'

    main(image_file, encode_file, decode_file)