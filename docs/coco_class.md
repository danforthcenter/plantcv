## class `COCO`

A PlantCV object class for `COCO` format annotations.

`COCO` is used to store information about objects in a standardized format useful for machine learning and intergrating with AI tools.

Currently `COCO` objects are made by calling the class constructor (see examples).

We refer users to the [COCO data format documentation](https://cocodataset.org/#format-data) for details. Currently PlantCV only uses "Object" or "Stuff" type annotations.

**plantcv.COCO**(mask=None, **kwargs)

- **Parameters:**
  - source - Either a Labeled or Binary mask of objects of interest or a [plantcv.plantcv.Objects](objects.md) object. If provided then the COCO object will add image records and annotations from the mask.
  - \*\*kwargs - Other keyword arguments passed to attributes of the COCO instance. See details in Attributes section.
    - "description", "datetime", "date", and "time" are passed to the `info` attribute if provided.
	- "id", "name", and "url" are passed to the `licenses` attribute if provided.
	- "image_id", "license", "filename", and "date_captured" are passed  to the `images` attribute if provided.
	- "category_id", "iscrowd", and "image_id" are paseed to the `annotations` attribute if provided.

### Attributes

Attributes are accessed as `COCO_instance.`*attribute_name*

#### `info`

`coco.`**info** contains general information about the dataset as a dictionary. In addition to any user-supplied information a `coco` object will add "plantcv_version" and "plantcv_run_date" key value pairs to the `info` dictionary. Information can be added on initialization or through `coco.add_record`.

Common fields that may be required in downstream tools or for complete recordkeeping are "year", "version", "descriptor", "contributor", "url", and "date_created". Those fields can currently be added using `coco.add_record`.

#### `licenses`

`coco.`**licenses** is a list containing any licenses present in the dataset. This will be empty unless the user specifies license information either on initializing the `coco` object or through `coco.add_record`.

Common fields that may be required in downstream tools or for complete recordkeeping are "id", "name", and "url".

#### `images`

`coco.`**images** is a list containing dictionaries of image metadata for the images in a dataset.

Commonly required fields are "id", "width", "height", "file_name", and "date_captured". "id", "width", and "height" are set automatically within a `coco` instance, `file_name` and `date_captured` may need to be added manually on initialization or through `coco.add_record`. A "license" field can also be used to map an image to a particular usage license (ie, `coco.images[0]["licenses"]` should match an "id" value in some entry in the `coco.licenses` list of dictionaries.


#### `annotations`

`coco.`**annotations** is a list containing dictionaries of object annotations for the objects in each image in a dataset.

Commonly required fields are "category_id", "iscrowd", "image_id", and "bbox". By default `coco` objects will set "category_id" to 1 ("plant") and "iscrowd" to 0 if a keyword argument is not provided for them. The "bbox" field is calculated using an image mask either on initialization or through `coco.add_record`. Additional "segmentation" and "area" fields are also calculated internally.

#### categories

`coco.`**categories** is a list containing dictionaries of categories. Category dictionaries are added through `coco.add_record` and should include "id", and "name" fields with an optional "supercategory" field for nested categories.

By default all objects annotations are labeled with `category_id: 1` which corresponds to "plant" in the categories dictionary that is made on initialization or calling `coco.add_record`.

### Methods

Methods are callable as `COCO_instance.`*method*()

#### clear

`coco.`**clear** will reset each attribute of the `coco` object to an empty dictionary or list.

#### add_record

`coco.`**add_record** adds images and corresponding annotations.

- **coco.add_record**(*source=None, info=None, rights=None, category=None, \*\*kwargs*)

- **Parameters:**
  - source - Optional Binary or Labelled mask or an ROI, see initialization docs.
  - info - Optional dictionary of additional info data
  - rights - Optional dictionary of additional licenses data
  - category - Optional dictionary of additional category data
  - \*\*kwargs
	- See initialization docs

#### append

`coco.`**append** adds images/annotations/data from another `coco` object into the current object.

- **coco.append**(*other*)

- **Parameters:**
  - other - Another `coco` object.

#### save

`coco.`**save** writes the `coco` object to a json file.

- **coco.save**(*filename, mode="a"*)

- **Parameters:**
  - filename - Name of file to save.
  - mode - Mode to write the file with, either "a" (the default) to append or "w" to (over)write.

#### load

`coco.`**load**(*filename*)

- **coco.load**(*filename*)

- **Parameters:**
  - filename - Name of coco json file to load data from
