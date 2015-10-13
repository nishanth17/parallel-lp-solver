import numpy as np

""" This file contains a bunch of common matrix operations used
	by both the LP solvers. """

def getItem(A, i , j):
	""" Returns the element in the ith row and jth column of A"""
	return A.item((i, j))

def dot(u, v):
	""" Returns the dot product of vectors u and v """
	return getItem(np.vdot(u,v), 0, 0)

def numNumRows(A):
	""" Returns the number of rows in the matrix A """
	return A.shape[0]

def numNumColumns(A):
	""" Returns the number of columns in the matrix A """
	return A.shape[1]

def getRow(A, i):
	""" Returns the ith row of the matrix A as a vector """
	return np.squeeze(np.asarray(A[i,:]))

def getColumn(A, j):
	""" Returns the jth column of the matrix A as a vector """
	return np.squeeze(np.asarray(A[:,j]))

def matrixVectorProduct(A,v):
	""" Returns the product of a matrix A and a vector v as a vector """
	return getRow(np.dot(A,v), 0)

