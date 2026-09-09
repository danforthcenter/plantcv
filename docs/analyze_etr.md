## Analyze Electron Transport Rate

Estimate mean and median electron transport rate (ETR).
Calculates `(Fq’/Fm’) * AlphaL * PSI/PSIIratio * Actinic_light`. This requires [calculating alphaL](analyze_alphaL.md) and [calculating Fq'/Fm'](analyze_yii.md) before ETR can be calculated.

**plantcv.analyze.etr**(*actinic_light, psi_psii_ratio=0.5*)

**returns** None

- **Parameters:**
    - actinic_light - Light intensity in PAR
	- psi_psii_ratio - Light absorption ratio between photosynthesis 1 and 2. Defaults to 0.5.

- **Context:**
    - Used to calculate ETR after YII and AlphaL are calculated. This requires APH frames and the frames input to [`analyze.yii`](analyze_yii.md).

- **Example use:**
    - Below

- **Output data stored:** Data (mean_etr, median_etr) are stored to the [`Outputs` class](outputs.md) when this function is run.

```python
from plantcv import plantcv as pcv

# calculate ETR
pcv.analyze.etr(actinic_light=10)
# check results
pcv.outputs.observations["plant_1"]["mean_etr"]["values"]

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/analyze/etr.py)
