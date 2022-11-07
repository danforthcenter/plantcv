import pytest
from plantcv.learn.cli import main


def test_run_naive_bayes_bad_imgdir():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", "does-not-exist",
                "--maskdir", "does-not-exist",
                "--outdir", "does-not-exist"]
    with pytest.raises(IOError):
        main()


def test_run_naive_bayes(tmpdir):
    """Test for PlantCV."""
    # Temp directory
    cache = tmpdir.mkdir("sub")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", "does-not-exist",
                "--maskdir", "does-not-exist",
                "--outdir", "does-not-exist"]
    with pytest.raises(IOError):
        main()
