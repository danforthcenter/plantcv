"""Write hyperspectral image data to a file."""
import os
from plantcv.plantcv import __version__ as version


def write_data(filename, spectral_data):
    """Write hyperspectral image data to a file.
    Parameters:
    -----------
    filename        = str,
        Name of file to write
    spectral_data   = plantcv.plantcv.classes.Spectral_data,
        Hyperspectral data object

    Returns:
    --------
    None
    """
    filename = os.path.splitext(filename)[0]

    # create header
    lines, samples, bands = spectral_data.array_data.shape
    dtype_dict = {'B': "1", 'h': "2", 'i': "3", 'f': "4", 'd': "5", 'F': "6",
                  'D': "9", 'H': "12", 'I': "13", 'l': "14", 'L': "15"}
    wavelengths = list(spectral_data.wavelength_dict.keys())
    with open(filename+'.hdr', mode='w') as f:
        f.write('ENVI\n')
        f.write(f'; this file was created using PlantCV version {version}\n')
        f.write(f'; original file: {spectral_data.filename}\n')
        f.write('interleave = bil\n')
        f.write(f'samples = {samples}\n')
        f.write(f'lines = {lines}\n')
        f.write(f'bands = {bands}\n')
        f.write(f'byte order = {spectral_data.byte_order}\n')
        f.write(f'file type = {spectral_data.file_type}\n')
        f.write(f'header offset = {spectral_data.header_offset}\n')
        f.write(f'data type = {dtype_dict[spectral_data.array_data.dtype.char]}\n')
        f.write(f'wavelength units = {spectral_data.wavelength_units}\n')
        if spectral_data.default_bands is not None:
            db_string = ",".join([str(band) for band in spectral_data.default_bands])
            f.write(f'default bands = {{{db_string}}}\n')
        f.write('wavelength = {\n')
        for wl in wavelengths[:-1]:
            f.write(f'{wl},\n')
        f.write(f'{wavelengths[-1]}\n')
        f.write('}')

    # create raw binary file containing the hyperspectral array values
    with open(filename+'.raw', mode='w+b') as f:
        f.write(spectral_data.array_data.transpose(0, 2, 1).tobytes(order='C'))
