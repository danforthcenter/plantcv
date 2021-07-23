# Tutorials

<style>
    div.card {
        margin: 5px;
        border: 1px solid #000;
        float: left;
        width: 200px;
        height: 350px;
    }
    div.card:hover {
        border: 2px solid #000;
    }
    div.card img {
        width: 100%;
        height: auto;
        padding: 5px;
    }
    div.card-title {
        padding: 5px;
        text-align: left;
    }
    div.card-title h6 {
        margin-bottom: 1px;
    }
    div.card-tags {
        padding: 5px;
        font-size: small;
    }
    div.card-button {
        padding: 5px;
        width: 125px;
    }
    div.card-filter-div {
        padding-bottom: 50px;
    }
</style>

<div class="card-filter-div">
    <label for="card-filter">Filter tutorials by tag:</label>
    <select name="card-filter" id="card-filter" onchange="filterCards(this.value)">
        <option value="show all">Show all</option>
    </select>
</div>

<!--VIS Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/vis_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/vis_tutorial/vis_tutorial_card_img.png?raw=true" alt="VIS tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant RGB image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, shape analysis, color analysis, height analysis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/vis_tutorial/vis_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--VIS-NIR Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/vis_nir_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/vis_nir_tutorial/vis_nir_tutorial_card_img.jpg?raw=true" alt="VIS-NIR tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant RGB dual RGB-NIR image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, Near-infrared, shape analysis, NIR analysis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/vis_nir_tutorial/vis_nir_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--NIR Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/nir_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/nir_tutorial/nir_tutorial_card_img.jpg?raw=true" alt="NIR tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant NIR image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, Near-infrared, shape analysis, NIR analysis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/nir_tutorial/nir_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Photosynthesis Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/psII_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/photosynthesis_tutorial/photosynthesis_tutorial_card.jpg?raw=true" alt="PSII tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant PSII (Fv/Fm) workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, Chlorophyll fluorescence, Fv/Fm analysis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/photosynthesis_tutorial/psII_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Thermal Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/thermal_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/thermal_tutorial/thermal_tutorial_card.jpg?raw=true" alt="Thermal tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Thermal image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, top-view, thermal infrared, thermal analysis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/thermal_tutorial/thermal.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Hyperspectral Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/hyperspectral_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/hyperspectral_tutorial/hyperspectral_tutorial_card.jpg?raw=true" alt="Hyperspectral tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Hyperspectral image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, hyperspectral, spectral index</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/hyperspectral_tutorial/hyperspectral_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Naive Bayes Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/machine_learning_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/naive_bayes_tutorial/naive_bayes_tutorial_card.png?raw=true" alt="Naive Bayes tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Naive Bayes Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant leaf, infection, classification, machine learning</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/naive_bayes_tutorial/machine_learning.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Multi-plant tools Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/multi-plant_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/multi_plant_tutorial/multi_plant_tutorial_card.png?raw=true" alt="Multi-plant tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Tools for Multi-Plant Analysis</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, RGB, shape analysis, brassica</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/multi_plant_tutorial/multi_plant_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Arabidopsis Multi-plant Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/arabidopsis_multi_plant_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/arabidopsis_multi_plant_tutorial/multi_plant_tutorial_card.png?raw=true" alt="Multi-plant tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Arabidopsis Multi-Plant Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, RGB, shape analysis, arabidopsis</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/arabidopsis_multi_plant_tutorial/arabidopsis_multiplant_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Seed Analysis Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/seed_analysis_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/seed_analysis_tutorial/seed_analysis_tutorial_card.jpg?raw=true" alt="Seed analysis tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Seed Analysis Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: seed, seed analysis, shape analysis, color analysis, seed count, quinoa</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/seed_analysis_tutorial/seed-analysis-workflow.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Morphology Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/morphology_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/morphology_tutorial/morphology_tutorial_card.png?raw=true" alt="Morphology tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Morphology Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, leaf/stem segmentation, leaf angle, leaf length</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/morphology_tutorial/morphology_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Sorghum Morphology Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/sorghum_morphology_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/new_side_view_morphology_tutorial/side_morphology_tutorial_card.png?raw=true" alt="Morphology tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Sorghum Shape and Morphology Analysis</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, shape analysis, leaf angle analysis, stem and branch segmentation, leaf length, leaf curvature, leaf tangent angle, sorghum</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/new_side_view_morphology_tutorial/morphology_analysis_side_view_workflow.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Color correction Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/transform_color_correction_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/color_correction_tutorial/color_correction_tutorial_card.png?raw=true" alt="Color correction tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Color Correction Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: color card, color correction</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/color_correction_tutorial/color_correct_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Input-Output Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/input_output_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/input_output_tutorial/input_output_tutorial_card.jpg?raw=true" alt="Input-output tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Input-Output Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: open image, save image, save plot</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/input_output_tutorial/input_output.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Threshold tools Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/threshold_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/threshold_tutorial/threshold_tutorial_card.png?raw=true" alt="Thresholding tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Thresholding Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, threshold methods</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/threshold_tutorial/threshold.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Updated Threshold Tools Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/threshold_tools_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/new_mask_tutorial/mask_tutorial_card.jpg?raw=true" alt="Thresholding tools tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Tools for Thresholding Plant Data</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, threshold methods, binary mask</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/new_mask_tutorial/create_binary_mask_tutorial.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--ROI Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/roi_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/roi_tutorial/roi_tutorial_card.png?raw=true" alt="ROI tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Region of Interest Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: region of interest, ROI</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/roi_tutorial/roi_package.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<!--Watershed Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/watershed_segmentation_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-binder/blob/master/notebooks/watershed_segmentation_tutorial/watershed_segmentation_tutorial_card.png?raw=true" alt="Watershed tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Watershed Segmentation Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, top-view, RGB, watershed segmentation, leaf segmentation</span>
    </div>
    <div class="card-button">
        <a href="https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/watershed_segmentation_tutorial/segmentation.ipynb"><img src="https://mybinder.org/badge_logo.svg"></a>
    </div>
</div>

<script type="text/javascript">
    function getTags() {
        var tag_list = [];
        var card_tags = document.getElementsByClassName("card-tags");
        for (var i = 0; i < card_tags.length; i++) {
            tags = card_tags[i].innerText;
            tags = tags.replace("Tags: ", "").split(", ");
            tag_list.push(...tags);
        }
        let unique_tags = [...new Set(tag_list)];
        addTagsToSelect(unique_tags);
    }
    function addTagsToSelect(tags) {
        var select_menu = document.getElementById("card-filter");
        for (var i = 0; i < tags.length; i++) {
            var opt = document.createElement("option");
            opt.text = tags[i];
            opt.value = tags[i];
            select_menu.add(opt);
        }
    }
    function filterCards(tag) {
        var cards;
        cards = document.getElementsByClassName("card");
        for (var i = 0; i < cards.length; i++) {
            var tags = cards[i].getElementsByClassName("card-tags")[0].getElementsByTagName("span")[0].innerText;
            tags = tags.replace("Tags: ", "").split(", ");
            if (tags.includes(tag)) {
                cards[i].style.display = "block";
            } else if (tag === 'show all') {
                cards[i].style.display = "block";
            } else {
                cards[i].style.display = "none";
            }
        }
    }
    window.addEventListener('load', getTags())
</script>
