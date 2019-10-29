# class hyperspec_img:
#
#     """PlantCV parameters class
#     Keyword arguments/parameters:
#     device       = device number. Used to count steps in the pipeline. (default: 0)
#     debug        = None, print, or plot. Print = save to file, Plot = print to screen. (default: None)
#     debug_outdir = Debug images output directory. (default: .)
#     :param device: int
#     :param debug: str
#     :param debug_outdir: str
#     :param line_thickness: numeric
#     :param dpi: int
#     :param text_size: float
#     """
#
#     def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5, dpi=100, text_size=0.55,
#                  text_thickness=2):
#         self.device = device
#         self.debug = debug
#         self.debug_outdir = debug_outdir
#         self.line_thickness = line_thickness
#         self.dpi = dpi
#         self.text_size = text_size
#         self.text_thickness = text_thickness

from plantcv.plantcv.hyperspectral.read_data import _find_closest
from plantcv.plantcv.hyperspectral.read_data import read_data
from plantcv.plantcv.hyperspectral.extract_index import extract_index
from plantcv.plantcv.hyperspectral.analyze_spectral import analyze_spectral

# add new functions to end of lists
__all__ = ["read_data", "_find_closest", "extract_index", "analyze_spectral"]

