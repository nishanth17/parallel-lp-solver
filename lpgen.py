import os
import subprocess as sp
from time import time

""" Generates the LP matrix for various cases. This is kind of whack but whatever."""

CWD =  os.getcwd()
BASE = "/Users/nishanthmohan/Downloads/bim-1.0/Generators/"

rbg_dir, rbg_exec = "rbg/", "./rbg1"
hilo_dir, hilo_exec = "HiLo/", "./HiLo"
karz_dir, karz_exec = "Karz/", "./Karz"
rmfu_dir, rmfu_exec = "rmfu/", "./rmfu"


def parseEdges(output):
	""" Generates a list of edges """
	edges = []
	for e in output:
		e = e.split(" ")
		edge = int(e[1]), int(e[2])
		edges.append(edge)
	return edges


def getLPMatrix(edges):
	"""
	Generates the bipartite matching LP constraint matrix given a list of 
	edges. 

	Input:
		edges = list of edges 

	Output:
		LP constraint matrix for bipartite matching
	"""
	n = len(edges)
	A = [] # LP Matrix
	d1, d2 = {}, {} # A dictionary for each side of the bipartition

	# Bucket edges by the vertices they intersect
	for i in range(len(edges)):
		u, v = edges[i]

		if not u in d1:
			d1[u] = [i]
		else:
			d1[u].append(i)

		if not v in d2:
			d2[v] = [i]
		else:
			d2[v].append(i)

	# Generate LP matrix
	for l in d1.values():
		c = [0] * n
		for e in l:
			c[e] = 1
		A.append(c)

	for l in d2.values():
		c = [0] * n
		for e in l:
			c[e] =  1
		A.append(c)

	return A


def getEdgesForRBG(n, ene):
	""" Generates a random bipartite graph (RBG). 

		Input:
			n = Number of vertices in each set of the bipartition 
			ene = Expected number of edges per vertex 

		Output:
			A list of edges of the bipartite graph
	"""

	os.chdir(BASE + rbg_dir)
	process = sp.Popen([rbg_exec, str(n), str(ene)], stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
	output, error = process.communicate()
	os.chdir(CWD)
	
	output = output.split('\n')[4:-2]
	return parseEdges(output)


def getLPMatrixForRBG(n, ene):
	""" Generates a random bipartite graph (RBG). 

		Input:
			n = Number of vertices in each set of the bipartition 
			ene = Expected number of edges per vertex 

		Output:
			The LP constrainst matrix for an RBG. 
	"""

	edges = getEdgesForRBG(n, ene)
	return getLPMatrix(edges)


def getEdgesForHiLo(k, l, d, p, n):
	""" Generates a HiLo bipartite graph (RBG). 

		Input:
			k = Number of vertices in each piece
			l = Number of pieces
			d = half the maximal degree of X-node
			p = boolean that indicates whether to permute nodes randomly
			n = boolean that indicates whether to not permute edges randomly

		Output:
			The edges of a HiLo bipartite graph. 
	"""

	os.chdir(BASE + hilo_dir)
	e = [hilo_exec, str(k)]
	if l != 1:
		e.append("-l" + str(l))
	if d != 10:
		e.append("-d" + str(d))
	if p:
		e.append("-p")
	if n: 
		e.append("-n")

	process = sp.Popen(e, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
	output, error = process.communicate()
	os.chdir(CWD)

	op = output.split("\n")[2:-1]
	return parseEdges(op)


def getLPMatrixForHiLo(k, l = 1, d = 10, p = False, n = False):
	""" Generates a HiLo bipartite graph (RBG). 

		Input:
			k = Number of vertices in each piece
			l = Number of pieces
			d = half the maximal degree of X-node
			p = boolean that indicates whether to permute nodes randomly
			n = boolean that indicates whether to not permute edges randomly

		Output:
			The LP constraint matrix of a HiLo bipartite graph. 
	"""

	edges = getEdgesForHiLo(k, l, d, p, n)
	return getLPMatrix(edges)


if __name__ == "__main__":
	t = time()
	x = getLPMatrixForHiLo(300, 20, 6, True, True)
	print "Matrix Dimensions:", str(len(x)), "x", str(len(x[0]))
	print "Time:", time() - t
