from __future__ import division
from __future__ import print_function
import numpy as np
from scipy.optimize import minimize

class ColaborativeFiltering:
	def __init__(self):
		#Init with know data
		self.num_users = 3
		self.num_products = 5
		self.num_features = 4

		#X is the matrix with the products attributes
		self.X = np.matrix([[1, 0.01, 0, 0], [0.001, 1, 0, 0.001], [0, 0, 1, 0], [0, 0, 0, 1],[1,0.2,0,0]],dtype=np.float_)
		
		#Y is the scor matrix given by the users 
		self.Y = np.matrix([[0,2,3],[0,2,5],[2,0,0],[5,0,0],[0,4,0]],dtype=np.float_)

		#R(i,j) is 1 if the user j has rated product i
		self.R = np.matrix([[0,0,1],[0,1,1],[1,0,0],[1,0,0],[1,1,0]],dtype=np.float_)

		self.Theta = np.matrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],dtype=np.float_)


	#Objetive function to being optimized by colavorative filtering
	def cofiCostFunc(self,params, *args):
		"""Unfold the U and W matrices from params"""
		Y, R, num_users, num_products, num_features,l = args[0], args[1],args[2], args[3],args[4],args[5]

		aux = params.reshape((num_products + num_users, num_features))

		X = aux[0:num_products , :]

		Theta = aux[num_products:, :] 

		test = np.dot(X,Theta.transpose())
		test = test - Y
		test = np.multiply(test , R)
		test = np.power(test,2)
		test = test.sum()
		test = 0.5 * test

		J = 0;
		regularization = (l * 0.5) * np.power(X,2).sum() + np.power(Theta,2).sum()

		J = test# + regularization

		return J		

	#Analitical jacobian for the objetive function of colaborative filtering
	def jacobian(self,params, *args):
		Y, R, num_users, num_products, num_features,l = args[0], args[1],args[2], args[3],args[4],args[5]

		aux = params.reshape((num_products + num_users, num_features))

		X = aux[0:num_products , :]

		Theta = aux[num_products:, :] 

		#X_grad = (((X * Theta' - Y) .* R)* Theta) + lambda .* X;
		X_grad = np.dot(np.multiply(np.dot(X,Theta.transpose()), R),Theta)
		print(X_grad)
		#Theta_grad = ((X' * ((X * Theta' - Y) .* R))') +  lambda .* Theta;
		Theta_grad = np.multiply(np.dot(X.transpose(),np.dot(X,Theta.transpose()) - Y),R).transpose()
		print(Theta_grad)
		grad = np.concatenate((X_grad, Theta_grad), axis=0)

		print(grad)
		return grad

	#Whenever we rate a product for a user, we normalize with respect the mean to
	#avoid cold start problem
	def normalizeRatings(self):
		size = self.Y.shape
		m = size[0]
		n = size[1]

		Ymean = np.zeros((m,1),dtype=np.float)
		Ynorm = np.zeros((m,n),dtype=np.float)

		for i in range(0, m):
		    acum = 0
		    elements = 0
		    for j in range(0,n):
		    	if self.R[i,j] == 1:
		    		acum += self.Y[i,j]
		    		elements += 1
		    if elements == 0:
		    	Ymean[i] = 0
		    else:
		    	Ymean[i] = acum / elements

		    for j in range(0,n):
		    	if self.R[i,j] == 1:
		    		Ynorm[i,j] = self.Y[i,j] - Ymean[i]
		return Ymean,Ynorm


	def updateSystem(self,productId,userId,score):
		self.R[productId,userId] = 1
		additional = (self.Y,self.R,self.num_users,self.num_products,self.num_features,0.00001)

		x0 = np.concatenate((self.X, self.Theta), axis=0)

		res = minimize(fun=self.cofiCostFunc, args=additional, x0=x0, method='nelder-mead',
                options={'xtol': 1e-8, 'disp': False})
		X = res.x[0:self.num_products*self.num_features].reshape((self.num_products, self.num_features))
		Theta = res.x[self.num_products*self.num_features:].reshape((self.num_users, self.num_features))

		self.X = X
		self.Theta = Theta

	def rateProductsForUser(self,userId):
		Theta_i = self.Theta[userId,:]
		scores = np.dot(Theta_i, self.X.transpose())

		Ymean,_ = self.normalizeRatings()
		scores = scores + Ymean.transpose()

		indexes = np.argsort(scores)
		fliped = np.flip(indexes,1)

		res = np.asarray(fliped).reshape(-1)

		return res.tolist()

colaborativeSystem = ColaborativeFiltering()





