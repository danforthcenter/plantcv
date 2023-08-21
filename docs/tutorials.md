# Tutorials

<style>
    div.card {
        margin: 5px;
        border: 1px solid #000;
        float: left;
        width: 200px;
        height: 325px;
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
        <img src="https://github.com/danforthcenter/plantcv-tutorial-v4-VIS-single-plant/blob/main/tutorial_card.png?raw=true" alt="VIS tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant RGB image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, shape analysis, color analysis, height analysis</span>
    </div>
</div>

<!--VIS-NIR Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/vis_nir_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-vis-nir/blob/main/vis_nir_tutorial_card_img.jpg?raw=true" alt="VIS-NIR tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant RGB dual RGB-NIR image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, Near-infrared, shape analysis, NIR analysis</span>
    </div>
</div>

<!--Grayscale Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/grayscale_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-grayscale/blob/main/img/scaled_gray.png?raw=true" alt="Grayscale tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant Grayscale image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant leaf, top view, single plant, grayscale, grayscale analysis, </span>
    </div>
</div>

<!--Photosynthesis Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/psII_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-photosynthesis/blob/main/tutorial_card.png?raw=true" alt="PSII tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Single plant PSII (Fv/Fm) workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: photosynthesis, Fv/Fm, NPQ, chlorophyll, chl</span>
    </div>
</div>

<!--Thermal Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/thermal_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-thermal/blob/main/tutorial_card.png?raw=true" alt="Thermal tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Thermal image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, top-view, thermal infrared, thermal analysis</span>
    </div>
</div>

<!--Hyperspectral Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/hyperspectral_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-hyperspectral/blob/main/tutorial_card.jpg?raw=true" alt="Hyperspectral tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Hyperspectral image workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: maize, corn, kernel, hyperspectral, spectral index</span>
    </div>
</div>

<!--Hyperspectral SMF Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/hyperspectral_smf_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-hyperspectral-smf-detection/blob/main/tutorial_card.jpg?raw=true" alt="Hyperspectral SMF tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Hyperspectral SMF workflow</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: Hyperspectral, Spectral Match Filter, Disease, Leaves, Machine Learning</span>
    </div>
</div>

<!--Naive Bayes Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/machine_learning_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-machine-learning/blob/main/naive_bayes_tutorial_card.png?raw=true" alt="Naive Bayes tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Naive Bayes Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant leaf, infection, classification, machine learning</span>
    </div>
</div>

<!--Multi-plant tools Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/multi-plant_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-v4-multiobject/blob/main/tutorial_card.png?raw=true" alt="Multi-plant tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Tools for Multi-Plant Analysis</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, RGB, shape analysis, brassica</span>
    </div>
</div>

<!--Arabidopsis Multi-plant Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/arabidopsis_multi_plant_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-arabidopsis-tray/blob/main/tutorial_card.png?raw=true" alt="Multi-plant tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Arabidopsis Multi-Plant Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, multi-plant, RGB, shape analysis, arabidopsis</span>
    </div>
</div>

<!--Seed Analysis Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/seed_analysis_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-seeds/blob/main/seed_analysis_tutorial_card.png?raw=true" alt="Seed analysis tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Seed Analysis Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: seed, seed analysis, shape analysis, color analysis, seed count, quinoa</span>
    </div>
</div>


<!--Sorghum Morphology Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/morphology_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-morphology/blob/main/tutorial_card.png?raw=true" alt="Morphology tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Sorghum Shape and Morphology Analysis</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, shape analysis, leaf angle analysis, stem and branch segmentation, leaf length, leaf curvature, leaf tangent angle, sorghum</span>
    </div>
</div>

<!--Color correction Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/transform_color_correction_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-color-correction/blob/main/tutorial_card.png?raw=true" alt="Color correction tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Color Correction Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: color card, color correction</span>
    </div>
</div>

<!--Input-Output Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/input_output_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-input-output/blob/main/tutorial_card.jpg?raw=true" alt="Input-output tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Input-Output Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: open image, save image, save plot</span>
    </div>
</div>

<!--Segmentation Tutorials-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/threshold_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-threshold/blob/main/tutorial_card.png?raw=true" alt="Segmentation tutorials" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Thresholding Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, side-view, RGB, threshold methods, seed, background subtraction, naive bayes, machine learning, segmentation</span>
    </div>
</div>

<!--ROI Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/roi_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-roi/blob/main/tutorial_card.png?raw=true" alt="ROI tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Region of Interest Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: region of interest, ROI</span>
    </div>
</div>

<!--Watershed Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/watershed_segmentation_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-tutorial-watershed/blob/main/tutorial_card.png?raw=true" alt="Watershed tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Watershed Segmentation Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: plant shoot, single plant, top-view, RGB, watershed segmentation, leaf segmentation</span>
    </div>
</div>

<!--Homology Tutorial-->
<div class="card" style="display:block">
    <a target="_blank" href="" onclick="location.href=this.href.replace('tutorials', 'tutorials/homology_tutorial');return false;">
        <img src="https://github.com/danforthcenter/plantcv-homology-tutorials/blob/main/plm_tutorial_card.png?raw=true" alt="Watershed tutorial" width="600" height="auto">
    </a>
    <div class="card-title">
        <h6>Pseudo-landmark Homology Tutorial</h6>
    </div>
    <div class="card-tags">
        <span><strong>Tags</strong>: pseudo-landmarking, homology, morphometrics, setaria</span>
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
