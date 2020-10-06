import dask_jobqueue
from dask.distributed import Client, progress
from subprocess import call


# Process images using multiprocessing
###########################################
def _process_images_multiproc(job):
    call(job)


# Create a dask local or distributed cluster
###########################################
def create_dask_cluster(cluster, cluster_config):
    """Create a dask cluster and return the cluster client
    Inputs:
    cluster        = string-based name of cluster class
    cluster_config = dictionary of cluster configuration keywords/parameters

    Returns:
    client         = dask cluster client object

    :param cluster: str
    :param cluster_config: dict
    :return client: distributed.client.Client
    """
    # There is one decision point
    # If the requested cluster is a LocalCluster we get it from dask.distributed
    if cluster == "LocalCluster":
        # Create a local cluster client with n_workers
        client = Client(n_workers=cluster_config.get("n_workers"))
    # Otherwise the cluster is a class from dask_jobqueue (a distributed resource scheduler)
    else:
        # Retrieve the scheduler class from dask-jobqueue
        sched = vars(dask_jobqueue).get(cluster)
        # The user must request the scheduler by the correct name, otherwise stop
        if sched is None:
            raise ValueError(f"The cluster {cluster} is not LocalCluster or a valid dask-jobqueue cluster.")
        # Configure the job scheduler by passing the cluster_config dictionary as keyword/value arguments
        drm = sched(**cluster_config)
        # Create a client for the cluster
        client = Client(drm)
    return client


# Process jobs using a dask cluster
###########################################
def multiprocess(jobs, client):
    """Process jobs using a dask cluster.
    Inputs:
    jobs   = list of jobs where each job is a list of workflow scripts and parameters
    client = dask cluster client object

    :param jobs: list
    :param client: distributed.client.Client
    """
    # Keep a list of job futures
    processed = []
    # Submit the jobs to the scheduler
    for job in jobs:
        # Submit individual job
        processed.append(client.submit(_process_images_multiproc, job))
    # Watch job progress and print a progress bar
    progress(processed)
    # Each job outputs results to disk so we do not need to gather results here
    client.shutdown()
###########################################
