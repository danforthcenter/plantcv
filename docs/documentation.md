## Documentation

PlantCV documentation is hosted on [Read the Docs](https://readthedocs.org/). 
Using Read the Docs allows the documentation to be versioned along with
the code. Because Read the Docs supports static content build tools like
[Mkdocs](http://www.mkdocs.org/), documentation can be written in simple
Markdown format that will be built into HTML automatically whenever a 
new version of code is pushed to the PlantCV GitHub repository.

### Updating PlantCV documentation

Follow the [contribution guide](CONTRIBUTING.md) to learn how to `fork` a
copy of the PlantCV repository, edit files, and generate a `pull`
request to merge your updates back into the main repository. Changes to
PlantCV should generally be done in the `dev` branch, which corresponds
to the `latest` version of the documentation on Read the Docs.

The documentation files are all located in the `docs` folder. If you are
editing existing documentation, the Markdown files can be edited in any
plain text editor or in the GitHub web interface. See [here](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
for an overview of Markdown format.

When adding new documentation, a new Markdown file should be added to
the `docs` folder with a descriptive name. If the documentation page
will include any images, these should be added to as subfolder specific
to the new documentation within the `docs/img` subdirectories. To keep
the size of the repository down, please only use `jpeg` images at a
maximum width of `400px` unless there is a specific need for a different
format or size. Please see other existing documentation files for
general style guidelines. Finally, new documentation files need to be
referenced in the `mkdocs.yml` file in the main repository folder. This
is done by adding the new file as a node in the table of contents tree.
In the example below a new documentation file was added to the
Documentation, Tutorials, and Library sections.

```
pages:
- Home: index.md
- Documentation:
  - Installation: installation.md
  - 'New general documentation': new_doc.md
  - Tutorials:
    - 'VIS pipeline': vis_tutorial.md
    - 'New tutorial': new_tutorial.md
  - Library:
    - 'Analyze color': analyze_color.md
    - 'New function': new_function.md
```

`mkdocs` can be used to test that the new documentation can be built
correctly locally before submitting to GitHub. From the root of a local
plantcv repository clone:

```
mkdocs build --theme readthedocs --site-dir _site
```

A clean build will output the messages:

```
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: plantcv/_site
```

The `_site` folder (ignored by git) will contain the static HTML files
that can be viewed with a web browser to double check that the new
documentation build looks as intended.

Once a pull request is merged into the repository, a new
version of the documentation will be built automatically.
