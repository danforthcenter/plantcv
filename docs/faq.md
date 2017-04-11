
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
- Q: Does PlantCV work with OpenCV 3.x?
    - A: Not yet, but this is a major goal for future development.
    Work towards this goal will be coordinated
    via GitHub [issue #21](https://github.com/danforthcenter/plantcv/issues/21)
    and/or [milestone #1](https://github.com/danforthcenter/plantcv/milestone/1).
    <!-- Cf. duplicate, https://github.com/danforthcenter/plantcv/issues/130 -->
- Q: When will the next stable version of PlantCV be released?
    - A: Please see the [Milestones](https://github.com/danforthcenter/plantcv/milestones)
    page for target date estimates
    and the status of selected planned releases.


### Image acquisition
- Q: How should I grow plants and acquire images for quantitative processing?
    - A: This depends on your main question of interest,
    and is beyond the scope of the current PlantCV documentation.
    You may be be interested
    in a [review article](http://doi.org/10.1016/j.pbi.2015.02.006)
    written by the lead PlantCV developers
    or in the glossary and general advice
    offered by [Roeder et al. (2012)](http://doi.org/10.1242/dev.076414)
- Q: Can I use PlantCV to process photos taken with a Raspberry Pi camera?
    - A: Yes.
    <!-- This is related to the previous question. -->
    <!-- https://github.com/danforthcenter/plantcv/issues/137 -->
    As noted in the ['Getting started' section](index.md),
    PlantCV was designed to work flexibly
    with many types of imagery as possible.
    Several groups are processing Raspberry Pi images using PlantCV,
    and the developers enthusiastically use Raspberry Pi cameras
    for [outreach and training efforts](https://github.com/danforthcenter/outreach/network)
    and timelapse imaging.
    You can even run PlantCV directly on a Pi
    (installation instructions for Ubuntu
    should work well with Raspbian),
    though this is certainly not required.
    See also tutorials on the [DDPSC Maker Group site](http://maker.danforthcenter.org/).
- Q: Can PlantCV use information about the temporal relation of images
  for object tracking etc.?
    - A: Not at present.
    OpenCV includes tools for analyzing video data,
    so this could be added in the future.

### Other
We try to continually improve our documentation.
We have not (necessarily) written answers for the following questions.
Users are encouraged
to ask questions by [filing an issue](https://github.com/danforthcenter/plantcv/issues)
and also to submit candidate questions and answers
via pull request.

- Q: How is PlantCV structured?
- Q: How is PlantCV tested?
- Q: Does PlantCV follow [Semantic Version Numbering](http://semver.org/)
  for stable releases?
- Q: Is there a naming convention for PlantCV functions?
    - A: No, not at present.
    Please see the guide to contributing
    for some general advice on code style,
    PEP8 docstrings etc.
