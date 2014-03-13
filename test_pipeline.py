#!/usr/bin/python
import os, sys, traceback
import argparse
from random import randrange
import threading
import Queue
import subprocess
import string

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Test a plantcv image processing pipeline with specific or randomly selected images.")
  parser.add_argument("-d", "--dir", help="Input directory containing images.", required=True)
  parser.add_argument("-p", "--pipeline", help="Pipeline script.", required=True)
  parser.add_argument("-r", "--random", help="Select a random set of images from the input directory", action="store_true")
  parser.add_argument("-n", "--num", help="Number of random images to test. Only used with -r. Default = 10", type=int, default=10)
  parser.add_argument("-t", "--threads", help="Number of threads/CPU to use. Default = 1", type=int, default=1)
  parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

# Job queue
jobs = Queue.Queue()
results = Queue.Queue()
roi = '/home/mgehan/LemnaTec/roi.png'

### Image processing thread
class process(threading.Thread):
  def __init__(self, jobs, results):
    threading.Thread.__init__(self)
    self.jobs = jobs
    self.results = results
    
  def run(self):
    while True:
      job = self.jobs.get()
      
      p = subprocess.Popen(job)
      out = p.stdout
      
      self.results.put(out)
      self.jobs.task_done()

### Data return thread
class output(threading.Thread):
  def __init__(self, results):
    threading.Thread.__init__(self)
    self.results = results
  
  def run(self):
    while True:
      # Grab output from result queue
      data = self.results.get()
      print data
      self.results.task_done()

### Main
def main():
  # Get options
  args = options()
  
  # Spawn jobs thread pool
  for i in range(args.threads):
    job_thread = process(jobs, results)
    job_thread.setDaemon(True)
    job_thread.start()
  
  # Single result thread
  # necessary so results get printed out one at a time
  result_thread = output(results)
  result_thread.setDaemon(True)
  result_thread.start()

  # Read input directory
  images = os.listdir(args.dir)
  
  if args.random:
    for i in range(0,args.num):
      img = images[randrange(0,len(images) - 1)]
      job = string.join(["python", args.pipeline, '-i', img, '-m', roi], ' ')
      jobs.put(job)
      print job
  else:
    for img in images:
      jobs.put("echo " + img)
  
  jobs.join()
  results.join()
  #while True:
  #  if not queue.empty():
  #    val = queue.get()
  #    print val, "\n"
  #  time.sleep(2)

if __name__ == '__main__':
  main()