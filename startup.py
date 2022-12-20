import Dashboard
import multiprocessing
import api


jobs = []
jobs.append(multiprocessing.Process(target=api.start))
jobs.append(multiprocessing.Process(target=Dashboard.start))


for job in jobs:

    job.start()