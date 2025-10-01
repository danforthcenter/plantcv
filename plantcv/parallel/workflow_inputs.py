import argparse
import os
from shutil import move


class WorkflowInputs:
    """Class for setting workflow inputs in Jupyter."""

    def __init__(self, images: list, names: str, result: str, outdir: str = ".", writeimg: bool = False,
                 debug: str = None, **kwargs):
        """Configure input variables for a PlantCV workflow.

        Keyword arguments:
        images = A list of one or more image files.
        names = A comma-delimited list containing a unique name for each image.
        result = An output JSON or CSV filename.
        outdir = An output directory for saved images (default = '.').
        writeimg = Save output images (default = False).
        debug = Set debug mode to None, 'print', or 'plot' (default = None).
        kwargs = Additional, user-defined workflow inputs.
        """
        self.result = result
        self.outdir = outdir
        self.writeimg = writeimg
        self.debug = debug
        self.__dict__.update(kwargs)
        self.__dict__.update(_name_images(names=names, img_list=images))


class workflow_inputs:
    """Class for parsed PlantCV workflow command-line options"""

    def __init__(self, *other_args):
        """Configure input variables"""
        parser = argparse.ArgumentParser(description="PlantCV user workflow.")
        parser.add_argument("images", help="Input image files.", type=str, nargs="+", metavar="IMAGES")
        parser.add_argument("--names", help="A unique name mapped to each input image.", required=True)
        parser.add_argument("--result", help="Output workflow results file.", required=True, dest="_result")
        parser.add_argument("--checkpoint", help="Logical, to Checkpoint or not.", required=True)
        parser.add_argument("--tmpfile", help="Path to results temp file.", required=True)
        parser.add_argument("--outdir", help="Output directory for image files.", default=".")
        parser.add_argument("--writeimg", help="Save output images.", default=False, action="store_true")
        parser.add_argument("--debug", help="Turn on debug, prints/plot intermediate images.",
                            choices=[None, "print", "plot"], default=None)
        # Parse additional user-defined workflow inputs
        for arg in other_args:
            parser.add_argument(f"--{arg}", help="Additional, user-defined workflow input.", required=False)
        args = parser.parse_args()
        for key, value in args.__dict__.items():
            setattr(self, key, value)
        # name images
        images = self._name_images()
        self.__dict__.update(images)
        # start checkpointing if possible
        self.attempt()

    def _name_images(self):
        """Pair image names with image file paths"""
        # initialize new dictionary for image names and paths
        images = {}
        # Enumerate the list of names split from the input comma-delimited string
        for i, name in enumerate(self.names.split(",")):
            # Pair each name with the corresponding image file path
            images[name.lower()] = self.images[i]
        return images

    def attempt(self):
        """Write the attempting checkpoint file"""
        # write the attempt file
        if self.checkpoint.strip().lower() == "true":
            open(os.path.splitext(self.tmpfile)[0] + "_attempt", "w")

    def complete(self):
        """Write the attempting checkpoint file"""
        # delete the _attempted file, write the _completed file
        if self.checkpoint.strip().lower() == "true":
            move(os.path.splitext(self.tmpfile)[0] + "_attempt", os.path.splitext(self.tmpfile)[0] + "_complete")

    @property
    def result(self):
        # rename _attempt file to _complete
        self.complete()
        # once that is done, return hidden version of results
        return self._result

    @result.setter
    def result(self, new):
        self._result = new
