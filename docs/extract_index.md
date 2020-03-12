## Extract Index 

This function extracts an index from a hyperspectral datacube, which is a [`Spectral_data` class](Spectral_data.md) instance created while reading in with [readimage](read_image.md)
with `mode='envi'`. There is also a parameter to allow some flexibility 
on using wavelengths that are at least close to the wavelength bands require to calculate a specific index. 

**plantcv.hyperspectral.extract_index**(*array, index="NDVI", distance=20*)

**returns** calculated index array (instance of the `Spectral_data` class)

- **Parameters:**
    - array         - A hyperspectral datacube object, an instance of the `Spectral_data` class, (read in with [pcv.readimage](read_image.md) with `mode='envi'`)
    - index         - Desired index, either "ndvi" for normalized difference vegetation index, "gdvi" for green difference
    vegetation index, "savi" for soil adjusted vegetation index, "pri" for photochemical reflectance index, "aci" for anthocyanin content index, or "ari" for anthocyanin reflectance index.
    - distance      - Amount of flexibility (in nanometers) regarding using wavelengths that are 
    at least close to the wavelength bands require to calculate a specific index

- **Note:**
    - We are adding potential indices as needed by PlantCV contributors, however the functions added to PlantCV are shaped in large part 
    by the end users so please post feature requests (including a specific index), questions, and comments on the 
    [GitHub issues page](https://github.com/danforthcenter/plantcv/issues). 
- **Example use:**
    - Below
```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Extract NDVI index from the datacube 
ndvi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="NDVI", distance=20)

# Extract GDVI index from the datacube
gdvi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="GDVI", distance=20)

# Extract SAVI index from the datacube
savi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="SAVI", distance=20)

# Extract ARI index from the datacube
ari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="ARI", distance=20)

# Extract ACI index from the datacube 
aci_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="ACI", distance=20)

# Extract ARI index from the datacube 
ari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="ARI", distance=20)

# Extract CARI index from the datacube 
cari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="CARI", distance=20)

# Extract CI_REDEDGE index from the datacube 
ci_rededge_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="CI_REDEDGE", distance=20)

# Extract CRI1 index from the datacube 
cri1_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="CRI1", distance=20)

# Extract CRI2 index from the datacube 
cri2_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="CRI2", distance=20)

# Extract EVI index from the datacube 
evi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="EVI", distance=20)

# Extract MARI index from the datacube 
mari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="MARI", distance=20)

# Extract MCARI index from the datacube 
mcari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="MCARI", distance=20)

# Extract MTCI index from the datacube 
mtci_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="MTCI", distance=20)

# Extract NDRE index from the datacube 
ndre_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="NDRE", distance=20)

# Extract PSND_CHLA index from the datacube 
psnd_chla_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSND_CHLA", distance=20)

# Extract PSND_CHLB index from the datacube 
psnd_chlb_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSND_CHLB", distance=20)

# Extract PSND_CAR index from the datacube 
psnd_car_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSND_CAR", distance=20)

# Extract PSRI index from the datacube 
psri_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSRI", distance=20)

# Extract PSSR1 index from the datacube 
pssr1_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSSR1", distance=20)

# Extract PSSR2 index from the datacube 
pssr2_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSSR2", distance=20)

# Extract PSSR3 index from the datacube 
pssr3_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="PSSR3", distance=20)

# Extract RGRI index from the datacube 
rgri_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="RGRI", distance=20)

# Extract RVSI index from the datacube 
rvsi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="RVSI", distance=20)

# Extract SIPI index from the datacube 
sipi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="SIPI", distance=20)

# Extract SR index from the datacube 
sr_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="SR", distance=20)

# Extract VARI index from the datacube 
vari_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="VARI", distance=20)

# Extract VI_GREEN index from the datacube 
vi_green_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="VI_GREEN", distance=20)

# Extract WBI index from the datacube 
wbi_array  = pcv.hyperspectral.extract_index(array=spectral_data, index="WBI", distance=20)


```

**NDVI array image**

![Screenshot](img/tutorial_images/hyperspectral/NDVI_index.jpg)

**GDVI array image**

![Screenshot](img/tutorial_images/hyperspectral/gdvi.jpg)

**SAVI array image**

![Screenshot](img/tutorial_images/hyperspectral/savi_index.jpg)

**ARI array image**

![Screenshot](img/tutorial_images/hyperspectral/ari_index.jpg)

**ACI array image**

![Screenshot](img/tutorial_images/hyperspectral/aci_index.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/hyperspectral/extract_index.py)
