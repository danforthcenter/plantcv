## Updating PlantCV

The general procedure for updating PlantCV if you are using the `master` branch
cloned from the `danforthcenter/plantcv` repository is to update your local 
repository and reinstall the package.

If you are not sure that you have cloned the `danforthcenter/plantcv` repository
and are on the `master` branch, here is how you can tell:

```
cd plantcv

git remote -v

# You should see something like:
# origin	https://github.com/danforthcenter/plantcv.git (fetch)

git status

# You should see:
# On branch master
# nothing to commit, working directory clean
```

If the above is true, updating can be done simply by:

```
git pull

python setup.py install

# Or with sudo if needed
```

If you have put the cloned plantcv repository folder in your `PYTHONPATH` then
pulling alone is enough to update.

### Updating from v1 to v2

The setuptools installation method was not available in PlantCV v1, so users
put the `plantcv/lib` directory in their custom `PYTHONPATH`. In PlantCV v2, the
plantcv library directory is no longer in the lib directory, now it is in the 
main repository folder (`plantcv/plantcv`). If you want to continue to have
plantcv in your `PYTHONPATH` you will need to update by simply removing `lib`
from the path. You can also remove the lib folder after pulling the new version.
Git will automatically remove the `*.py` files but because we do not track the
`*.pyc` files they will remain behind and can technically be imported, which can
cause confusion.

For Linux/Unix, `PYTHONPATH` can be edited in `~/.bash_profile`, `~/.bashrc`,
`~/.profile`, `~/.cshrc`, `~/.zshrc`, etc. For Windows, right-click on My 
Computer/This PC and select Properties > Advanced system settings >
Environmental Variables... and edit the User variables entry for `PYTHONPATH`.

Also note that the method for parallelizing PlantCV has changed, please see the
new [parallel processing documentation](pipeline_parallel.md) for more details.

### Updating to v3

In order to support the installation of optional add-on subpackages, we converted
PlantCV to a [namespace package](https://packaging.python.org/guides/packaging-namespace-packages/).
To achieve this new funcitonality, existing functions had to be moved into a 
subpackage to maintain easy importing. To maintain previous behavior, PlantCV
analysis scripts simply need to have updated PlantCV import syntax. So if you were
previously doing something like:

```python
import plantcv as pcv
```

You would now do this instead:

```python
from plantcv import base as pcv
```

Another feature we will be rolling out for PlantCV v3 an update to the existing
package API. The goal is to make each PlantCV function easier to use. This will
be apparent in two ways at first. 1) all existing functions/functionality will 
remain intact but we will be adding deprecation warnings to outdated functions 
that are being replaced. 2) New functions will utilize a global parameters class
to inherit values for standard inputs like `debug` and `device` so that these 
values will not need to be explicitly input to each function. An instance of the
class `Params` as `params` is created automatically when PlantCV is imported and
it can be imported to set global defaults. For example, to change debug from
`None` to 'plot' or 'print':

```python
from plantcv import base as pcv
pcv.params.debug = "plot"
```

For more information, see the [Params](params.md) documentation.