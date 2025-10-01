from plantcv.parallel import WorkflowInputs, workflow_inputs
import os


def test_workflowinputs():
    """Test for PlantCV."""
    args = WorkflowInputs(images=["vis.png", "nir.png"], names="vis,nir", result="test.txt")
    assert args.vis == "vis.png" and args.nir == "nir.png"


def test_workflow_inputs():
    """Test for PlantCV."""
    import sys
    sys.argv = ["workflow.py", "--names", "vis", "--result", "test.txt", "--other", "otherval", "vis.png",
                "--checkpoint", "true", "--tmpfile", "example_tmp"]
    args = workflow_inputs(*["other"])
    assert args.vis == "vis.png"


def test_workflow_inputs_checkpoint(tmpdir):
    """Test for PlantCV."""
    tmp = tmpdir.mkdir("cache")
    os.chdir(tmp)
    import sys
    sys.argv = ["workflow.py", "--names", "vis", "--result", "test.txt", "--other", "otherval", "vis.png",
                "--checkpoint", "true", "--tmpfile", "example_tmp"]
    args = workflow_inputs(*["other"])
    # touch args.result to trigger complete method
    x = args.result
    # touch args.result setter
    args.result = x
    assert os.path.exists(os.path.join(tmp, "example_tmp_complete"))
