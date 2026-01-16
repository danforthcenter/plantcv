## Accessory Tools

Several accessory tools are provided with PlantCV. These tools are installed in your system or environment path or are
available by downloading/cloning the GitHub repository.

### Training machine learning models

`plantcv-train` is a command-line tool for training machine learning classifiers or other models in PlantCV. More
detail is provided in the [Machine Learning Tutorial](https://plantcv.org/tutorials/naive-bayes) but command/input details are
provided below:

```
usage: plantcv-train [-h] {naive_bayes,naive_bayes_multiclass, kmeans, tabulate_bayes_classes}

Subcommands:
    naive_bayes
        usage: plantcv-train naive_bayes [-h] -i IMGDIR -b MASKDIR -o OUTFILE [-p]
        
        optional arguments:
            -h, --help                       Show this help message and exit
            -i IMGDIR, --imgdir IMGDIR       Input directory containing images.
            -b MASKDIR, --maskdir MASKDIR    Input directory containing black/white masks.
            -o OUTFILE, --outfile OUTFILE    Trained classifier output filename.
            -p, --plots                      Make output plots.
        
    naive_bayes_multiclass
        usage: plantcv-train naive_bayes_multiclass [-h] -f FILE -o OUTFILE [-p]
        
        optional arguments:
            -h, --help                       Show this help message and exit
            -f FILE, --file FILE             Input file containing a table of pixel RGB values sampled for each input 
                                             class.
            -o OUTFILE, --outfile OUTFILE    Trained classifier output filename.
            -p, --plots                      Make output plots.
    kmeans
        usage: plantcv-train kmeans [-h] -i IMGDIR -k CATEGORIES -o OUTFILE [-r] [-p] [-s] [-n] [--sampling] [--seed] [--n_init]

        optional arguments:
            -h, --help                      Show this message and exit
            -i IMGDIR, --imgdir IMDIR       Input directory containing images. 
            -k INT, --categories INT        Number of classification categories.
            -o OUTFILE, --out OUTFILE       Trained model output path and filename.
            -r PREFIX, --prefix PREFIX      File prefix for training images.
            -p INT, --patch_size INT        Patch size.
            -s INT, --sigma INT             Severity of Gaussian blur, sigma.
            --sampling FLOAT                Fraction of pixels sampled per image for patch extraction
            --seed INT                      Random seed for reproducibility
            -n INT, --num_imgs INT          Number of images in training directory to use.
            --n_init INT                    Number of Kmeans random initiations  

usage: plantcv-train tabulate_bayes_classes [-h] -i FILE -o OUTFILE

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
                        Input file containing a table of pixel RGB values sampled for each input class.
  -o OUTFILE, --outfile OUTFILE
                        Output tab-delimited table file.

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/learn/cli.py)

#### Tabulate Naive Bayes Classes

For `plantcv-learn tabulate_bayes_classes`the input file should have class names preceded by the "#" character. RGB values can be pasted directly from ImageJ without reformatting. E.g.:

```
#plant
96,154,72	95,153,72	91,155,71	91,160,70	90,155,67	92,152,66	92,157,70
54,104,39	56,104,38	59,106,41	57,105,43	54,104,40	54,103,35	56,101,39	58,99,41	59,99,41
#background
114,127,121	117,135,125	120,137,131	132,145,138	142,154,148	151,166,158	160,182,172
115,125,121	118,131,123	122,132,135	133,142,144	141,151,152	150,166,158	159,179,172

```

### PlantCV Parallel

`plantcv-sample` is a command-line tool for sampling image data from a path or [parallel configuration file](parallel_config.md).

Testing a workflow on small test set (that ideally spans time and/or treatments) can speed up workflow optimization and 
test it on other images in the dataset to determine how robust the workflow will be. The random image sampler can help 
identify 'problem images' before running a workflow in parallel over a large set of images. This
tool can handle LemnaTec structured output in addition to a flat file directory.
An output directory will be created if it does not already exist. The number of 
random images requested must be less than or equal to the number of images in the source directory if using phenofront or phenodata formats.

```
usage: plantcv-sample [-h] -s SOURCE -o OUTPUT_DIRECTORY -n NUMBER

optional arguments:
  -h, --help                                      Show this help message and exit
  -s SOURCE, --source                             Input image directory or path to configuration file
  -o OUTPUT_DIRECTORY, --outdir OUTPUT_DIRECTORY  Output directory.
  -n NUMBER, --number NUMBER                      Number of images to randomly select. (default=100)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/sample_images.py)


`plantcv-run-workflow` is a command-line tool for parallel processing of user-defined PlantCV workflows. It is used to
process metadata and execute custom workflows on each image in a dataset. More detail is provided in the 
[Workflow Parallelization Tutorial](pipeline_parallel.md).

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/cli.py)
