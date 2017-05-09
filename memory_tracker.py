import psutil
import os

_proc = psutil.Process(os.getpid())
#_baseline = _baseline = psutil.virtual_memory().used >> 10
_baseline = _proc.memory_info().rss >> 10
_peak = 0



def rebase():
	global _peak, _baseline
	#_baseline = psutil.virtual_memory().used >> 10


	_peak = 0

def update_peak():
	global _peak
	#mem = psutil.virtual_memory().used >> 10
	mem = _proc.memory_info().rss >> 10
	_peak = max(_peak, (abs(mem-_baseline)))

def getPeak():
	global _peak
	return _peak
