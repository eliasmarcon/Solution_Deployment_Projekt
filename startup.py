import Dashboard
import FastAPI
import multiprocessing
import api.api as api


jobs = []
jobs.append(multiprocessing.Process(target=FastAPI.start))
jobs.append(multiprocessing.Process(target=api.start))
jobs.append(multiprocessing.Process(target=Dashboard.start))


for job in jobs:

    job.start()