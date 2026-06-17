## Plot Delta E

This function creates an interactive bar chart visualizing per-chip Delta E (color difference) values from a color checker card. Each bar is colored by a standard interpretation category: green (<1) indicates imperceptible differences, progressing through yellow (<2, <10) to orange and red (<49, >49) for increasingly noticeable differences. Reference lines at the category boundaries are drawn for quick visual assessment. Standard chip color swatches from the target color matrix are displayed below the x-axis to aid chip identification.

**plantcv.qc.plot_deltaE**(*deltaE_matrix*)

**returns** chart, an altair.vegalite.v5.api.LayerChart object

- **Parameters:**
    - deltaE_matrix - numpy.ndarray of per-chip Delta E values, shaped to match the color card layout (e.g., (6, 4) for a 24-chip Macbeth card or (3, 5) for a 15-chip AstroBotany card), as returned from [`pcv.transform.deltaE`](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/detect_color_card.py).

- **Context:**
    - Used to evaluate the quality of color calibration by visualizing how closely observed chip colors match their expected values. Lower Delta E values indicate better color fidelity. This function is best used during workflow development to interactively inspect calibration results before and after color correction or between different color correction methods.

- **Example use:**
    - Below

**Dataset image:**

![Screenshot](img/documentation_images/qc_plot_delta_e/input.png)

```python

from plantcv import plantcv as pcv
from plantcv.plantcv.transform.detect_color_card import deltaE

# Calculate Delta E values for each chip relative to the standard color matrix
de_matrix = deltaE(rgb_img=img, color_chip_size="classic")

# Plot the Delta E values
chart = pcv.qc.plot_deltaE(deltaE_matrix=de_matrix)

```

**Delta E bar chart:**

![Screenshot](img/documentation_images/qc_plot_delta_e/uncalibrated_output.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/qc/plot_delta_e.py)
