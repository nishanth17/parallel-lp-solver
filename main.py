import lpgen
import ourStuff
import zhuOrecchia
from time import time

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

eps = 1/10.0
MAX_ITERATIONS = 10000


def solveLPforRBG(n, ene):
	A = lpgen.getLPMatrixForRBG(n, ene)
	print "\nRuning bipartite matching LP on a graph with"\
		,str(2*n), "nodes and", str(len(A[0])), "edges\n"

	print "\nRunning Zhu-Orecchia...\n"
	x1, obj1 = zhuOrecchia.posLPSolver(A, eps, verbose = False, max_iterations = MAX_ITERATIONS)

	print "\nRunning our stuff...\n"
	x2, obj2 = ourStuff.posLPSolver(A, eps, verbose = False, max_iterations = MAX_ITERATIONS)
	
	k = np.arange(0, len(obj2))
	pl.plot(k, obj1, 'bo')
	pl.plot(k, obj2, 'rx')
	pl.show()


if __name__ == "__main__":
	t = time()
	solveLPforRBG(6, 2)
	print "\nTime:", time() - t