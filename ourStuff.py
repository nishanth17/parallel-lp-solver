import time
import numpy as np
from numpy import linalg as LA
import matrixUtils as utils

""" Our LP solver """

EPS_THRESHOLD = 0.5
RESOLUTION = 1000

def truncO(v, eps):
	if v > 1: return 1
	a = abs(v)
	if a <= eps: return 0
	else: return v

def trunc(v, t, eps):
	e = truncO(v, eps)
	a = abs(e)
	lb = pow(2, t) * eps # eps * 2^t
	ub = lb * 2 # eps * 2^(t+1)
	if a > lb and a <= ub: return e
	else: return 0


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
	alpha = mu / 20

	# NOTE: The base of the log has to be 2!!
	W = np.log(1 / eps) / np.log(2) # log(1/eps) = number of groups

	w = int(np.ceil(W))
	T = int(np.ceil(10 * W * np.log(2*n) / (alpha * eps)))
	T = min(max_iterations, T)

	if verbose: 
		print "Matrix dimensions =", A.shape
		print "Number of iterations =", T, "\n"
		print "Nmber of groups =", w
		time.sleep(1)

	x = np.zeros(n)
	k = (1 - eps/2) / n
	for i in range(n):
		x[i] = k / max_of_cols[i]

	obj_vals = np.array([])
	ref = np.zeros(n)
	for k in range(T+1):

		if k % RESOLUTION == 0:
			print "k =", str(k), "...."
			obj_vals = np.append(obj_vals, sum(x))

		t = np.random.randint(0, w)
		if verbose and k % RESOLUTION == 0: 
			print "1-Norm difference =", str(LA.norm(x - ref, 1))
			print "t =", t
			print "Bounds =", str(eps * pow(2,t)), "to", str(eps * pow(2,t+1))
			ref = x

		x_new = np.zeros(n)
		Ax = utils.matrixVectorProduct(A, x)
		y = np.exp((Ax - 1.0) / mu)
		t = np.random.randint(0, w)
		
		for i in range(n):
			v_i = 0 
			for j in range(m):
				v_i += utils.getItem(A, j, i) * y[j]

			v_i -= 1.0
			x_new[i] = x[i] * np.exp(-alpha * trunc(v_i, t, eps))
			if verbose and k % RESOLUTION == 0:
				print i, v_i, trunc(v_i, t, eps)
				pass

		x = x_new

	# Scale x back up
	x = x * beta / (1 + eps)
	return x.tolist(), obj_vals
	