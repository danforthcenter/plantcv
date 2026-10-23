# Tests for _hash_current_file
import os
import json
from plantcv.plantcv._globals import _hash_current_file


def test_hashing_python_file(tmpdir, monkeypatch):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, "test.py")
    with open(filename, "w", encoding='utf-8') as fp:
        data = "from plantcv import plantcv as pcv\npcv.read_image('my_image.png')"
        fp.write(data)
    # patch __main__ to point to a dummy python file
    import __main__ as main
    monkeypatch.setattr(main, "__file__", filename)
    # call _hash_current_file to trigger python script option
    hc1 = _hash_current_file()
    assert hc1
    # make sure that the hash does change for small changes in a script
    filename2 = os.path.join(cache_dir, "test2.py")
    with open(filename2, "w") as fp:
        data = "from plantcv import plantcv as pcv\npcv.read_image('my_other_image.png')"
        fp.write(data)
    monkeypatch.setattr(main, "__file__", filename2)
    hc2 = _hash_current_file()
    assert hc1 != hc2


def test_hashing_notebook(tmpdir, monkeypatch):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, "test.ipynb")
    os.environ["JPY_SESSION_NAME"] = filename

    notebook1 = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "d1a897aa-d499-437c-8c22-5b6dc7876691",
                "metadata": {},
                "outputs": [],
                "source": [
                    "from plantcv import plantcv as pcv\n",
                    "pcv.read_image(\"my_image\")",
                ],
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(filename, "w") as f:
        json.dump(notebook1, f, indent=1, ensure_ascii=False)
        f.write("\n")

    import __main__ as main
    monkeypatch.setattr(main, "__file__", False)

    hc1 = _hash_current_file()
    assert hc1
    # make sure that the hash does not change for small changes in a notebook
    filename2 = os.path.join(cache_dir, "test2.ipynb")
    notebook1["cells"][0]["source"][1] = "pcv.read_image(\"my_other_image\")"

    with open(filename2, "w") as f:
        json.dump(notebook1, f, indent=1, ensure_ascii=False)
        f.write("\n")

    os.environ["JPY_SESSION_NAME"] = filename2
    hc2 = _hash_current_file()

    assert hc1 == hc2
