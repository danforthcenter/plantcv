# Plot the color values of a target and source color matrix
import os
import numpy as np
import pandas as pd
import altair as alt
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params


def quick_color_check(target_matrix, source_matrix, num_chips):
    """Plot the color values of a target and source color card matrix.

    Quickly plot target matrix values against source matrix values to determine
    over saturated color chips or other issues.

    Parameters:
    -----------
    source_matrix      = numpy.ndarray,
        an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
        of the source image
    target_matrix      = numpy.ndarray,
        an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
        of the target image
    num_chips          = int,
        number of color card chips included in the matrices (integer)

    Returns:
    --------
    p1                 = altair.vegalite.v5.api.Chart,
        an altair plot of the target and source color values
    """
    # Scale matrices to 0-255
    target_matrix = 255*target_matrix
    source_matrix = 255*source_matrix

    # Extract and organize matrix info
    tr = target_matrix[:num_chips, 1:2]
    tg = target_matrix[:num_chips, 2:3]
    tb = target_matrix[:num_chips, 3:4]
    sr = source_matrix[:num_chips, 1:2]
    sg = source_matrix[:num_chips, 2:3]
    sb = source_matrix[:num_chips, 3:4]

    # Create columns of color labels
    red = ["red"] * num_chips
    blue = ["blue"] * num_chips
    green = ["green"] * num_chips

    # Make a column of chip numbers
    chip = np.arange(0, num_chips).reshape((num_chips, 1))
    chips = np.vstack((chip, chip, chip))

    # Combine info
    color_data_r = np.column_stack((sr, tr, red))
    color_data_g = np.column_stack((sg, tg, green))
    color_data_b = np.column_stack((sb, tb, blue))
    all_color_data = np.vstack((color_data_b, color_data_g, color_data_r))

    # Create a dataframe with headers
    dataset = pd.DataFrame({'source': all_color_data[:, 0], 'target': all_color_data[:, 1],
                            'color': all_color_data[:, 2]})

    # Add chip numbers to the dataframe
    dataset['chip'] = chips
    dataset = dataset.astype({'color': str, 'chip': str, 'target': float, 'source': float})

    # Make the plot
    p1 = alt.Chart(dataset).mark_point(point=True).encode(
        x="target",
        y="source",
        color=alt.Color("color").scale(range=["blue", "green", "red"]),
        column="color"
        )

    _debug(visual=p1, filename=os.path.join(params.debug_outdir, 'color_quick_check.png'))

    return p1.interactive()
