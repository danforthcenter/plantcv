import argparse


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
        parser.add_argument("--checkpoint", help="Path to checkpointing csv file.", required=True)
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
        self.touch_checkpoint(value="attempted")

    def _name_images(self):
        """Pair image names with image file paths"""
        # initialize new dictionary for image names and paths
        images = {}
        # Enumerate the list of names split from the input comma-delimited string
        for i, name in enumerate(self.names.split(",")):
            # Pair each name with the corresponding image file path
            images[name.lower()] = self.images[i]
        return images

    def touch_checkpoint(self, value):
        """Edit the checkpoint file"""
        # I'd initially imagined working with the config, but maybe that isn't how this can work?
        # just need the path to the metadata file and a way to index the rows so I can write `value`
        #if os.path.exists(self.checkpoint):
            # find row, can do that by reading the outfile or by using the image name?
            # read csv (might be problematic if several read at once to edit?)
            # edit csv (could I do this outside of python more easily?)
            # write csv
        print("~Something~ to touch " + self.checkpoint + " and add '" + value + "' to 'checkpointing' column")

    @property
    def result(self):
        # getter function should only be called for saving results which can trigger end_checkpoint()
        # this would still need to know if there is information in the params.outputs, not if self._results is populated
        self.touch_checkpoint(value="completed")
        # once that is done, return hidden version of results
        return self._result

    @result.setter
    def result(self, new):
        self._result = new
