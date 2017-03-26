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

Also note that the method for parallelizing PlantCV has changed, please see the
new [parallel processing documentation](pipeline_parallel.md) for more details.
