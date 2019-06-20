import multiprocessing as mp
from subprocess import call


# Process images using multiprocessing
###########################################
def _process_images_multiproc(job):
    call(job)


# Multiprocessing pool builder
###########################################
def multiprocess(jobs, cpus):
    try:
        p = mp.Pool(processes=cpus)
        p.map(_process_images_multiproc, jobs)
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
        p.join()
        raise ValueError("Execution terminated by user\n")

###########################################
