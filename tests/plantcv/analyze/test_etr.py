import pytest
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.analyze.etr import etr


def test_etr():
    """Test for PlantCV."""
    outputs.clear()
    outputs.add_observation(sample="label1",
                                variable = 'yii_mean_t1',
                                trait='dummy yii',
                                method='dummy.method',
                                scale='none', datatype=float,
                                value=10, label='none')
    outputs.add_observation(sample="label1",
                                variable = 'alphaL_mean',
                                trait='dummy alpha',
                                method='dummy.alpha.method',
                                scale='none', datatype=float,
                                value=5, label='none')
    outputs.add_observation(sample="label1",
                                variable = 'yii_median_t1',
                                trait='dummy yii',
                                method='dummy.method',
                                scale='none', datatype=float,
                                value=10, label='none')
    outputs.add_observation(sample="label1",
                                variable = 'alphaL_median',
                                trait='dummy alpha',
                                method='dummy.alpha.method',
                                scale='none', datatype=float,
                                value=5, label='none')
    etr(10)
    assert outputs.observations["label1"]["mean_etr"]["value"] == 250


def test_etr_no_yii():
    """Test for PlantCV."""
    outputs.clear()
    outputs.add_observation(sample="label1",
                                variable = 'alphaL_mean',
                                trait='dummy alpha',
                                method='dummy.alpha.method',
                                scale='none', datatype=float,
                                value=5, label='none')
    outputs.add_observation(sample="label1",
                                variable = 'alphaL_median',
                                trait='dummy alpha',
                                method='dummy.alpha.method',
                                scale='none', datatype=float,
                                value=5, label='none')
    with pytest.raises(RuntimeError):
        etr(10)


def test_etr_no_alphaL():
    """Test for PlantCV."""
    outputs.clear()
    outputs.add_observation(sample="label1",
                                variable = 'yii_mean_t1',
                                trait='dummy yii',
                                method='dummy.method',
                                scale='none', datatype=float,
                                value=10, label='none')
    outputs.add_observation(sample="label1",
                                variable = 'yii_median_t1',
                                trait='dummy yii',
                                method='dummy.method',
                                scale='none', datatype=float,
                                value=10, label='none')
    with pytest.raises(RuntimeError):
        etr(10)
