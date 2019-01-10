
Some Frequently Asked Questions are collected here,
grouped by category.

<!-- Advice in box:
http://producingoss.com/en/getting-started.html#documentation -->

### Versions
Related pages: guides to
[installing PlantCV](installation.md),
[contributing](CONTRIBUTING.md),
and [updating documentation](documentation.md).

- Q: Which version of PlantCV should I use?
    - A: We suggest using the latest code from GitHub ('master' branch),
    as described in the installation instructions.
    If you are trying to reproduce the results from a specific manuscript,
    you may prefer to use one of the [stable releases](https://github.com/danforthcenter/plantcv/releases).
    These releases are assigned Digital Object Identifiers (DOI)
    and [archived](https://doi.org/10.5281/zenodo.595522)
    at Zenodo.org.
- Q: How should I cite PlantCV?
    - A: See the main ['About' page](http://plantcv.danforthcenter.org/pages/about.html).
    At minimum,
    you ought to cite
    the [original published description](http://doi.org/10.1016/j.molp.2015.06.005)
    of PlantCV.
    You should ideally reference the specific version used
    (by number and DOI)
    and publications related to specific features added
    since the initial release.
- Q: What version(s) of Python and OpenCV does PlantCV work with?
    - A: PlantCV currently works with both Python 2.7 and 3+ and OpenCV 2 and 3. Python 2.7 can be used with
    either OpenCV 2 or 3 but Python 3 can only be used with OpenCV 3. Our recommended configuration is
    Python 3 and OpenCV 3. In the future, Python 2 and OpenCV 2 
    support will end but removing support is not currently on our roadmap.
- Q: When will the next stable version of PlantCV be released?
    - A: Please see the [Milestones](https://github.com/danforthcenter/plantcv/milestones)
    page for target date estimates
    and the status of selected planned releases.


### Image acquisition
- Q: How should I grow plants and acquire images for quantitative processing?
    - A: This depends on your main question of interest,
    and is beyond the scope of the current PlantCV documentation. We do provide some 
    [general considerations](analysis_approach.md), but you may be be interested
    in a [review article](http://doi.org/10.1016/j.pbi.2015.02.006)
    written by the lead PlantCV developers,
    a [practical guide](https://doi.org/10.1071/FP12028)
    on growth conditions by Poorter et al. (2012),
    or a [glossary and general advice](https://doi.org/10.1242/dev.076414)
    by Roeder et al. (2012).
- Q: Can I use PlantCV to process photos taken with a Raspberry Pi camera?
    - A: Yes.
    <!-- This is related to the previous question. -->
    <!-- https://github.com/danforthcenter/plantcv/issues/137 -->
    As noted in the ['Getting started' section](index.md),
    PlantCV was designed to work flexibly
    with many types of imagery as possible.
    Several groups are processing Raspberry Pi images using PlantCV,
    and PlantCV developers enthusiastically use Raspberry Pi cameras
    for [outreach and training efforts](https://github.com/danforthcenter/outreach/network)
    and timelapse imaging.
    See the [example scripts](https://github.com/danforthcenter/apps-phenotyping)
    associated with a [recently submitted protocol note](https://doi.org/10.1101/183822).
    You can even run PlantCV directly on a Pi
    (installation instructions for Ubuntu
    should work well with Raspbian),
    but this is certainly not required.
    See also tutorials on the [DDPSC Maker Group site](http://maker.danforthcenter.org/).
- Q: Can PlantCV use information about the temporal relation of images
  for object tracking etc.?
    - A: Not at present.
    OpenCV includes tools for analyzing video data,
    so this could be added in the future.
- Q: My plants are touching,
  and getting merged into a single object.
  What can I do?
    - A: Not much, for now.
      <!-- https://github.com/danforthcenter/plantcv/issues/142 -->
      PlantCV is geared toward images of well-spaced plants.
      Facilities for drawing custom boundaries
      exist in other tools,
      and could in principle be added.

### Other
We try to continually improve our documentation.
We have not (necessarily) written answers for the following questions.
Users are encouraged
to ask questions by [filing an issue](https://github.com/danforthcenter/plantcv/issues)
and also to submit candidate questions and answers
via pull request.

- Q: How is PlantCV structured?
    - A: As of v3.0 we are following semantic version numbering.
- Q: How is PlantCV tested?
    - A: Unit tests are in the 'tests' directory
    in the root of the source tree.
    We use the Travis Continuous Integration tool
    to [monitor status](https://travis-ci.org/danforthcenter/plantcv)
    and test pull requests
    for breaking changes.
- Q: Does PlantCV follow [Semantic Version Numbering](http://semver.org/)
  for stable releases?
     - A: Not entirely.
      Major releases are mostly based on new features.
      We try to avoid changes that break compatibility
      between minor version releases.
- Q: Is there a naming convention for PlantCV functions?
    - A: No, not at present.
    Please see the [guide to contributing](CONTRIBUTING.md)
    for some general advice on code style,
    PEP8 docstrings etc.
