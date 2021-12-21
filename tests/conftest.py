import pytest
import os
import matplotlib
import json

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        self.workflowconfig_template_file = os.path.join(self.datadir, "workflowconfig_template.json")
        self.flat_imgdir = os.path.join(self.datadir, "flat_imgdir")
        self.workflow_script = os.path.join(self.datadir, "plantcv-script.py")

    # JSON loading helper function
    def load_json(self, json_file):
        """JSON loader helper function.
        Inputs:
        json_file = JSON filepath

        Returns:
        data      = Dictionary of JSON data

        :param json_file: str
        :return data: dict
        """
        with open(json_file, "r") as fp:
            data = json.load(fp)
            return data

    def workflowconfig_template(self):
        """Load WorkflowConfig template from file."""
        return self.load_json(json_file=self.workflowconfig_template_file)


@pytest.fixture(scope="session")
def test_data():
    return TestData()
