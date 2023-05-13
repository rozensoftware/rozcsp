import psutil
import os

def memory_usage():
    """return the memory usage in MB"""
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem