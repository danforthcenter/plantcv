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


def workflow_inputs(*other_args) -> argparse.Namespace:
    """Parse PlantCV workflow command-line options.

    Keyword arguments:
    other_args = additional, user-defined workflow inputs.

    Outputs:
    args = an argparse ArgumentParser object with command-line keyword attributes.

    :param other_args: list
    :return args: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="PlantCV user workflow.")
    parser.add_argument("images", help="Input image files.", type=str, nargs="+", metavar="IMAGES")
    parser.add_argument("--names", help="A unique name mapped to each input image.", required=True)
    parser.add_argument("--result", help="Output workflow results file.", required=True)
    parser.add_argument("--outdir", help="Output directory for image files.", default=".")
    parser.add_argument("--writeimg", help="Save output images.", default=False, action="store_true")
    parser.add_argument("--debug", help="Turn on debug, prints/plot intermediate images.",
                        choices=[None, "print", "plot"], default=None)
    # Parse additional user-defined workflow inputs
    for arg in other_args:
        parser.add_argument(f"--{arg}", help="Additional, user-defined workflow input.", required=False)
    args = parser.parse_args()

    images = _name_images(names=args.names, img_list=args.images)
    args.__dict__.update(images)
    return args


def _name_images(names: str, img_list: list) -> dict:
    """Pair image names with image file paths.

    Keyword arguments:
    names = a comma-delimited string of unique names.
    img_list = a list of image file paths.

    Outputs:
    images = a dictionary of name-image file path pairings.
    """
    images = {}
    # Enumerate the list of names split from the input comma-delimited string
    for i, name in enumerate(names.split(",")):
        # Pair each name with the corresponding image file path
        images[name.lower()] = img_list[i]
    return images
