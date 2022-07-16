from plantcv.parallel import WorkflowInputs, workflow_inputs


def test_workflowinputs():
    """Test for PlantCV."""
    args = WorkflowInputs(images=["vis.png", "nir.png"], names="vis,nir", result="test.txt")
    assert args.vis == "vis.png" and args.nir == "nir.png"


def test_workflow_inputs():
    """Test for PlantCV."""
    import sys
    sys.argv = ["workflow.py", "--names", "vis", "--result", "test.txt", "--other", "otherval", "vis.png"]
    args = workflow_inputs(*["other"])
    assert args.vis == "vis.png"
