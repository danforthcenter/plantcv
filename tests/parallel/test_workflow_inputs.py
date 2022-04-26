from plantcv.parallel import WorkflowInputs


def test_workflowinputs():
    args = WorkflowInputs(images=["vis.png", "nir.png"], names="vis,nir", result="test.txt")
    assert args.vis == "vis.png" and args.nir == "nir.png"
