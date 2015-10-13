import time
import numpy as np
import matrixUtils as utils
from numpy import linalg as LA

""" The Zhu-Orecchia LP solver """

EPS_THRESHOLD = 0.1
RESOLUTION = 1000

def trunc(v, eps):
	if v > 1: return 1
	a = abs(v)
	if a <= eps: return 0
	else: return v

def posLPSolver(A, eps, verbose = False, max_iterations = float("inf")):
	assert eps > 0 and eps <= EPS_THRESHOLD, "Invalid epsilon value"

	A = np.matrix(A)
	m = utils.numNumRows(A)
	n = utils.numNumColumns(A)

	beta = float("inf") # the scaling factor so that min(max[A[:,j]]) = 1
	max_of_cols = np.zeros(n)
	for i in range(n):
		max_of_cols[i] = np.max(utils.getColumn(A, i))
		if max_of_cols[i] < beta:
			beta = max_of_cols[i]

	# Scale down A to ensure that min(max[A[:,j]]) = 1
	A /= beta
	max_of_cols /= beta

	mu = eps / (4 * np.log(m*n/eps))
	alpha = eps * mu / 4
	T = int(np.ceil(6 * np.log(2*n) / (alpha * eps)))
	T = min(max_iterations, T)
	obj_vals = np.array([])
	ref = np.zeros(n)

	x = np.zeros(n)
	k = (1 - eps/2) / n
	for i in range(n):
		x[i] = k / max_of_cols[i]

	if verbose:
		print "A"
		print A
		print "Matrix dimensions =", A.shape
		print "Number of iterations =", T, "\n"
		print "mu = ", mu
		print "x0 =", x
		time.sleep(1)

	for k in range(T+1):
		x_new = np.zeros(n)
		Ax = utils.matrixVectorProduct(A, x)
		y = np.exp((Ax - 1.0) / mu)

		if k % RESOLUTION == 0:
			print "k =", str(k), "...."
			obj_vals = np.append(obj_vals, sum(x))

		if verbose and k % RESOLUTION == 0: 
				print "1-Norm difference =", str(LA.norm(x - ref, 1))
				ref = x
		
		for i in range(n):
			v_i = 0 
			for j in range(m):
				v_i += utils.getItem(A, j, i) * y[j]
				
			v_i -= 1.0
			x_new[i] = x[i] * np.exp(-alpha * trunc(v_i, eps))
			if verbose and k % RESOLUTION == 0:
				print i, v_i, trunc(v_i, eps)

		x = x_new

	# Scale x back up
	x = x * beta / (1 + eps)
	return x.tolist(), obj_vals

