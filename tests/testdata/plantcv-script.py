#!/usr/bin/env python

from plantcv import plantcv as pcv
from plantcv.parallel import workflow_inputs

# Run main program.
args = workflow_inputs(*["other"])
_ = pcv.__version__

pcv.outputs.save_results(filename=args.result)
