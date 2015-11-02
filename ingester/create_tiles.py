from collections import namedtuple
import logging
from math import floor, ceil

from ingester.utils import get_file_extents, execute

_LOG = logging.getLogger(__name__)

TileFile = namedtuple('TileFile', 'filename minlon maxlon minlat maxlat')

EXAMPLE_CONFIG = {
    'output_dir': '/short/v10/dra547/tmp/today',
    'srs': 'EPSG:4326',
    'grid_lats': [],
    'grid_lons': [],
    'directory_structure': '{product_name}/{x}_{y}/{year}/{product_name}_{sensor_name}_{x}_{y}_{timestamp}.{extension}',
    'file_extension': 'nc'
}


def stack_bands_together(src_files, basename):
    """
    Take a list of src files of equal position and time, and stack them into a single VRT

    :param src_files: []
    :param basename: str
    :return: filename string
    """
    scene_vrt = '{}.vrt'.format(basename)

    execute(['gdalbuildvrt', '-separate', scene_vrt] + src_files)

    return scene_vrt


def calculate_expanded_extents(filename):
    """

    :param filename:
    :return:
    """
    _LOG.debug("Calculating expanded extents for {}".format(filename))
    extents = get_file_extents(filename)
    _LOG.debug("Input extents: {}".format(extents))
    xmin = str(floor(min(p[0] for p in extents)))
    ymin = str(floor(min(p[1] for p in extents)))
    xmax = str(ceil(max(p[0] for p in extents)))
    ymax = str(ceil(max(p[1] for p in extents)))

    expanded_extents = xmin, ymin, xmax, ymax
    _LOG.debug("Expanded extents are: {}".format(expanded_extents))

    return expanded_extents


def reproject_and_expand(input_vrt, basename, output_extents, target_srs="EPSG:4326"):
    reprojected_vrt = '{}.{}.vrt'.format(basename, target_srs.lower().replace(':', ''))
    target_pixel_res = "0.00025"

    extents_args = []
    if output_extents:
        extents_args = ['-te'] + list(output_extents)

    execute(['gdalwarp',
             '-t_srs', target_srs,
             '-of', 'VRT',
             '-tr', target_pixel_res, target_pixel_res,  # Pixel resolution x,y (Fraction of a degree)
             '-tap',  # Force to nest within the grid definition
             '-srcnodata', '-999',
             '-dstnodata', '-999'] +
            extents_args +
            [input_vrt, reprojected_vrt])
    return reprojected_vrt


def list_tile_files(csv_path):
    tile_files = []
    with open(csv_path, 'r') as csvfile:
        for line in csvfile:
            filename, minlon, maxlon, minlat, maxlat = line.split(';')
            minlon = int(float(minlon))
            minlat = int(float(minlat))

            tile_file = TileFile(filename, minlon, maxlon, minlat, maxlat)
            tile_files.append(tile_file)

    return tile_files


def create_tile_files(input_vrt, target_dir='.', pixel_size=4000,
                      output_format='NetCDF',
                      create_options=None):
    if create_options is None:
        create_options = ['FORMAT=NC4', 'COMPRESS=DEFLATE', 'ZLEVEL=1']
    csv_path = 'test.csv'

    # Make list like ['-co', 'FORMAT=NC4', '-co', 'COMPRESS=DEFLATE', '-co', 'ZLEVEL=1']
    create_options = sum([['-co', option] for option in create_options], [])
    pixel_size = str(pixel_size)

    execute(['gdal_retile.py', '-v', '-targetDir', target_dir,
             '-ps', pixel_size, pixel_size,
             '-of', output_format, '-csv', csv_path, '-v'] + create_options + [input_vrt])

    return list_tile_files(csv_path)


def calc_output_filenames(tile_files, format_string, dataset):
    """
    Read CSV generated by gdal_retile and return list of tile mappings

    Example format string:
    {product_name}/{x}_{y}/{year}/{product_name}_{sensor_name}_{x}_{y}_{timestamp}.{file_extension}


    Additional attributes are:
    x = minimum longitude in file
    y = minimum latitude in file

    :param tile_files: List of TileFiles
    :type tile_files: list of TileFile
    :param format_string: String describing new filename
    :param dataset: attributes to use in the format string
    :rtype: list[(existing_filename, new_filename)]
    """
    renames = []
    for tile_file in tile_files:
        base, middle, extension = tile_file.filename.split('.')

        # FIXME DODGY
        file_attributes = {
            'x': tile_file.minlon,
            'y': tile_file.minlat,
            'extension': extension,
            'ga_label': dataset.ga_label
        }

        new_filename = format_string.format(**file_attributes)

        renames.append((tile_file.filename, new_filename))
    return renames


def create_tiles(input_files, basename, tile_options=None):
    """
    Run a series of steps to turn a list of input files into a grid of stacked tiles

    :param input_files:
    :param basename:
    :param tile_options:
    :rtype: list[TileFile]
    """
    if tile_options is None:
        tile_options = []

    src_files = [str(path) for path in input_files]

    combined_vrt = stack_bands_together(src_files, basename)
    tile_aligned_extents = calculate_expanded_extents(combined_vrt)
    expanded_reprojected_vrt = reproject_and_expand(combined_vrt, basename, output_extents=tile_aligned_extents)
    created_tiles = create_tile_files(expanded_reprojected_vrt, **tile_options)

    return created_tiles

# Nearest neighbour vs convolution. Depends on whether discrete values
# -r resampling_method