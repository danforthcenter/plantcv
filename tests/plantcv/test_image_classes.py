import copy
import pickle
from unittest import mock
import cv2
import numpy as np
import pytest
from plantcv.plantcv.classes import Image, Color, Gray, Mask, LabeledMask, Spectral


LEAF_KINDS = ["color", "gray", "mask", "labeled_mask", "spectral"]


def make_image(kind):
    """Create a valid image of the requested kind."""
    if kind == "color":
        data = np.arange(4 * 6 * 3, dtype=np.uint8).reshape(4, 6, 3)
        return Color(data, uri="color.png", channels=("B", "G", "R"))
    if kind == "gray":
        return Gray(np.arange(24, dtype=np.uint8).reshape(4, 6), uri="gray.png", channel="G")
    if kind == "mask":
        data = np.zeros((4, 6), dtype=np.uint8)
        data[1:3, 2:5] = 255
        return Mask(data, uri="mask.png")
    if kind == "labeled_mask":
        return LabeledMask(np.arange(24, dtype=np.int32).reshape(4, 6), uri="labels.png")
    data = np.arange(4 * 6 * 5, dtype=np.float32).reshape(4, 6, 5)
    return Spectral(data, uri="cube.hdr", wavelengths=[450, 500, 550, 650, 750],
                    default_wavelengths=[480, 540, 710], metadata={"sensor": "test"})


def meta(img):
    """Return the metadata of an image as a dictionary."""
    return {name: getattr(img, name) for name in img._meta}


@pytest.fixture(params=LEAF_KINDS)
def leaf(request):
    """Fixture returning one valid image of each kind."""
    return make_image(request.param)


@pytest.fixture
def color():
    """Fixture returning a BGR Color image."""
    return make_image("color")


# Construction and validation
def test_image_is_abstract():
    """Test that the Image base class cannot be constructed."""
    with pytest.raises(TypeError):
        Image(np.zeros((2, 2)), uri="img.png")


def test_leaf_construction(leaf):
    """Test that each image kind is an Image and an ndarray with its uri set."""
    assert isinstance(leaf, Image)
    assert isinstance(leaf, np.ndarray)
    assert leaf.uri is not None


def test_uri_default():
    """Test that uri defaults to None."""
    assert Gray(np.zeros((2, 2))).uri is None


def test_kinds_are_siblings():
    """Test that no image kind is an instance of another."""
    assert not isinstance(make_image("mask"), Gray)
    assert not isinstance(make_image("labeled_mask"), Gray)


@pytest.mark.parametrize("build", [
    lambda: Color(np.zeros((2, 2, 3))),
    lambda: Color(np.zeros((2, 2)), channels=("B", "G")),
    lambda: Color(np.zeros((2, 2, 3)), channels=("B", "G")),
    lambda: Color(np.zeros((2, 2, 3)), channels=("B", "B", "R")),
    lambda: Color(np.zeros((2, 2, 3)), channels=("B", "G", 3)),
    lambda: Gray(np.zeros((2, 2, 3))),
    lambda: Mask(np.zeros((2, 2, 3), dtype=bool)),
    lambda: Mask(np.zeros((2, 2), dtype=np.float64)),
    lambda: Mask(np.array([[0, 1], [255, 0]], dtype=np.uint8)),
    lambda: LabeledMask(np.zeros((2, 2, 3), dtype=int)),
    lambda: LabeledMask(np.zeros((2, 2), dtype=float)),
    lambda: Spectral(np.zeros((2, 2, 3))),
    lambda: Spectral(np.zeros((2, 2)), wavelengths=[500, 600]),
    lambda: Spectral(np.zeros((2, 2, 3)), wavelengths=[500, 600]),
])
def test_validation_errors(build):
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError):
        build()


def test_mask_from_bool():
    """Test that a boolean mask is stored as uint8 0/255."""
    mask = Mask(np.array([[True, False], [False, True]]))
    assert mask.dtype == np.uint8
    assert np.array_equal(mask, np.array([[255, 0], [0, 255]], dtype=np.uint8))


def test_view_bypasses_validation():
    """Test that viewing a plain array as an image kind leaves metadata as None."""
    img = np.zeros((2, 2, 3)).view(Color)
    assert isinstance(img, Color)
    assert img.channels is None
    assert img.uri is None


def test_color_channels_stored_as_tuple():
    """Test that channel labels are stored as a tuple."""
    img = Color(np.zeros((2, 2, 3)), channels=["R", "G", "B"])
    assert img.channels == ("R", "G", "B")


# Prototype failure modes
@pytest.mark.parametrize("op", [
    lambda c: c[..., ::-1],
    lambda c: c[:, 0, :],
    lambda c: c[np.ones(c.shape[:2], dtype=bool)],
    lambda c: c[:, :, ::-1],
    lambda c: c[:, :, 0],
    lambda c: c[0],
    lambda c: c[None],
    lambda c: c[[0, 1]],
    lambda c: np.mean(c, axis=2),
    lambda c: c.sum(axis=2),
    lambda c: c > 100,
    lambda c: c + 1,
])
def test_channel_changing_ops_return_ndarray(color, op):
    """Test that operations that may change channel meaning return a plain ndarray."""
    assert type(op(color)) is np.ndarray


def test_pickle_round_trip(leaf):
    """Test that pickling keeps the image kind, data, and metadata."""
    restored = pickle.loads(pickle.dumps(leaf))
    assert type(restored) is type(leaf)
    assert np.array_equal(restored, leaf)
    assert meta(restored) == meta(leaf)


def test_spectral_crop_keeps_metadata():
    """Test that cropping a Spectral image keeps all of its metadata."""
    cube = make_image("spectral")
    crop = cube[1:3, 2:5]
    assert isinstance(crop, Spectral)
    assert crop.wavelengths == cube.wavelengths
    assert crop.wavelength_units == "nm"
    assert crop.metadata == {"sensor": "test"}
    assert crop.default_wavelengths == [480, 540, 710]


# Propagation
@pytest.mark.parametrize("op", [
    lambda img: img[1:3, 2:5],
    lambda img: img[1:3],
    lambda img: img[::-1],
    lambda img: img[:, ::-1],
    lambda img: img[::2, ::2],
    lambda img: img[()],
])
def test_spatial_slicing_keeps_kind(leaf, op):
    """Test that crops, flips, and strides keep the image kind and metadata."""
    result = op(leaf)
    assert type(result) is type(leaf)
    assert meta(result) == meta(leaf)


def test_scalar_indexing(leaf):
    """Test that indexing a single element returns a scalar."""
    index = (0,) * leaf.ndim
    assert not isinstance(leaf[index], np.ndarray)


@pytest.mark.parametrize("op", [
    lambda img: np.dstack([img, img]),
    lambda img: np.concatenate([img, img]),
    lambda img: np.where(img > 0, img, 0),
    lambda img: np.copy(img),
    lambda img: np.flip(img, axis=0),
    lambda img: img.reshape(-1),
    lambda img: img.T,
    lambda img: img.transpose(),
    lambda img: img.swapaxes(0, 1),
    lambda img: img.ravel(),
    lambda img: img.flatten(),
    lambda img: img[:1].squeeze(),
    lambda img: img.argmax(axis=0),
    lambda img: img.argmin(axis=0),
    lambda img: img.argsort(axis=0),
    lambda img: img.argpartition(1, axis=0),
    lambda img: img.take([0], axis=0),
    lambda img: img.repeat(2, axis=0),
    lambda img: img.diagonal(),
    lambda img: img.compress([True, False], axis=0),
    lambda img: img.dot(np.ones(img.shape[-1])),
    lambda img: img.byteswap(),
    lambda img: img.astype(np.uint16).getfield(np.uint8),
    lambda img: img.flat[:3],
    lambda img: img.view(np.int8),
    lambda img: img.view(dtype=np.uint8),
])
def test_ops_return_ndarray(leaf, op):
    """Test that NumPy functions and shape-changing methods return a plain ndarray."""
    assert type(op(leaf)) is np.ndarray


def test_split_returns_ndarrays(color):
    """Test that NumPy functions returning a list convert every element to ndarray."""
    parts = np.split(color, 2, axis=0)
    assert isinstance(parts, list)
    assert all(type(p) is np.ndarray for p in parts)


def test_namedtuple_results_keep_fields():
    """Test that NumPy functions returning a named tuple keep its fields."""
    gray = Gray(np.eye(3))
    result = np.linalg.svd(gray)
    assert type(result.U) is np.ndarray
    assert type(result.S) is np.ndarray


def test_choose_returns_ndarray():
    """Test that choose returns a plain ndarray."""
    labels = LabeledMask(np.zeros((2, 2), dtype=int))
    assert type(labels.choose([1, 2])) is np.ndarray


def test_flat_assignment(leaf):
    """Test that assigning through flat writes to the image data."""
    leaf.flat = 0
    assert not np.any(leaf)
    assert isinstance(leaf, Image)


def test_view_without_dtype_keeps_kind(leaf):
    """Test that a view without a dtype keeps the image kind and metadata."""
    result = leaf.view()
    assert type(result) is type(leaf)
    assert meta(result) == meta(leaf)
    assert type(leaf.view(np.ndarray)) is np.ndarray


def test_inplace_ufunc_keeps_kind(leaf):
    """Test that in-place operations keep the image kind and metadata."""
    expected = meta(leaf)
    original = leaf
    leaf += 1
    assert leaf is original
    assert meta(leaf) == expected


def test_ufunc_multiple_outputs(color):
    """Test that ufuncs with multiple outputs return the original output objects."""
    out1 = Color(np.zeros(color.shape), uri="a", channels=color.channels)
    out2 = np.zeros(color.shape)
    result = np.divmod(color, 2, out=(out1, out2))
    assert result[0] is out1
    assert result[1] is out2
    assert isinstance(out1, Color)


@pytest.mark.parametrize("op", [
    lambda img: img.copy(),
    lambda img: img.astype(float),
    lambda img: copy.copy(img),
    lambda img: copy.deepcopy(img),
])
def test_copies_keep_kind(leaf, op):
    """Test that copies and dtype conversions keep the image kind and metadata."""
    result = op(leaf)
    assert type(result) is type(leaf)
    assert meta(result) == meta(leaf)


def test_deepcopy_copies_metadata():
    """Test that deepcopy does not share mutable metadata."""
    cube = make_image("spectral")
    clone = copy.deepcopy(cube)
    assert clone.metadata == cube.metadata
    assert clone.metadata is not cube.metadata


def test_opencv_returns_ndarray(color):
    """Test that OpenCV accepts image kinds and returns a plain ndarray."""
    blurred = cv2.GaussianBlur(color, (3, 3), 0)
    assert type(blurred) is np.ndarray
    assert blurred.shape == color.shape


def test_asarray_returns_ndarray(leaf):
    """Test that np.asarray returns a plain ndarray."""
    assert type(np.asarray(leaf)) is np.ndarray


# Color methods
def test_color_channel(color):
    """Test extracting a channel by label."""
    green = color.channel("G")
    assert type(green) is Gray
    assert green.channel == "G"
    assert green.uri == color.uri
    assert np.array_equal(green, np.asarray(color)[:, :, 1])


def test_color_channel_unknown(color):
    """Test that an unknown channel label raises ValueError."""
    with pytest.raises(ValueError):
        color.channel("H")


def test_color_reorder(color):
    """Test that reorder permutes the data and the labels."""
    rgb = color.reorder(("R", "G", "B"))
    assert type(rgb) is Color
    assert rgb.channels == ("R", "G", "B")
    assert rgb.uri == color.uri
    assert np.array_equal(rgb, np.asarray(color)[:, :, ::-1])
    assert np.array_equal(rgb.channel("R"), color.channel("R"))


@pytest.mark.parametrize("order", [("R", "G"), ("R", "G", "G"), ("R", "G", "X")])
def test_color_reorder_invalid(color, order):
    """Test that reorder rejects orders that are not a permutation of the channels."""
    with pytest.raises(ValueError):
        color.reorder(order)


# Spectral methods
def test_spectral_min_max():
    """Test the wavelength range properties."""
    cube = make_image("spectral")
    assert cube.min_wavelength == 450
    assert cube.max_wavelength == 750


def test_spectral_get_wavelength():
    """Test that get_wavelength returns the nearest band as a Gray image."""
    cube = make_image("spectral")
    band = cube.get_wavelength(640)
    assert type(band) is Gray
    assert band.channel == 650
    assert band.uri == cube.uri
    assert np.array_equal(band, np.asarray(cube)[:, :, 3])


def test_spectral_thumbnail_color():
    """Test that a 3-band thumbnail stacks the bands in BGR order."""
    data = np.stack([np.full((2, 2), v, dtype=np.uint8) for v in (10, 20, 30, 40, 50)], axis=-1)
    cube = Spectral(data, uri="cube.hdr", wavelengths=[480, 540, 600, 650, 710])
    thumb = cube.thumbnail()
    assert type(thumb) is Color
    assert thumb.channels == ("B", "G", "R")
    assert thumb.uri == "cube.hdr"
    assert thumb.channel("B")[0, 0] == 10
    assert thumb.channel("G")[0, 0] == 20
    assert thumb.channel("R")[0, 0] == 50


def test_spectral_thumbnail_gray():
    """Test that a 1-band thumbnail is a Gray image of the default band."""
    data = np.stack([np.full((2, 2), v, dtype=np.uint8) for v in (10, 20, 30)], axis=-1)
    cube = Spectral(data, uri="cube.hdr", wavelengths=[700, 800, 900], default_wavelengths=[800])
    thumb = cube.thumbnail()
    assert type(thumb) is Gray
    assert thumb.channel == 800
    assert thumb[0, 0] == 20


def test_spectral_default_rgb_range():
    """Test that RGB default wavelengths are used when the range covers 490 to 635."""
    cube = Spectral(np.zeros((2, 2, 2)), wavelengths=[490, 635])
    assert cube.default_wavelengths == [480, 540, 710]


def test_spectral_default_brightest_band_is_lazy():
    """Test that the brightest-band default is computed on first access, not on construction or crop."""
    data = np.zeros((4, 4, 3))
    data[:, :, 1] = 5
    with mock.patch("plantcv.plantcv.classes.np.sum", wraps=np.sum) as spy:
        cube = Spectral(data, wavelengths=[700, 800, 900])
        crop = cube[1:3, 1:3]
        assert spy.call_count == 0
        assert cube.default_wavelengths == [800]
        assert spy.call_count == 1
        assert cube.default_wavelengths == [800]
        assert spy.call_count == 1
    assert crop._default_wavelengths is None


def test_spectral_default_wavelengths_setter():
    """Test setting and resetting the default wavelengths."""
    cube = make_image("spectral")
    cube.default_wavelengths = (500, 600, 700)
    assert cube.default_wavelengths == [500, 600, 700]
    cube.default_wavelengths = None
    assert cube.default_wavelengths == [480, 540, 710]
