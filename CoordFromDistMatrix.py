import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#Used to convert distance matrix and allow for coordinate representation
#of nodes based on distance
def getMatrixDomainCoords():
	nodeCoords = []
	X = np.array([(0, 172, 145, 607, 329, 72, 312, 120),
	                (172, 0, 192, 494, 209, 158, 216, 92),
	                (145, 192, 0, 490, 237, 75, 205, 100),
	                (607, 494, 490, 0, 286, 545, 296, 489),
	                (329, 209, 237, 286, 0, 421, 49, 208),
	                (72, 158, 75, 545, 421, 0, 249, 75),
	                (312, 216, 205, 296, 49, 249, 0, 194),
	                (120, 92, 100, 489, 208, 75, 194, 0)
	              ])

	#Call to sklearn method written to convert distance matrices to node representations
	decomp = PCA(n_components=2)
	nodeCoords = decomp.fit_transform(X)

	#Assign node coordinates to lists of x and y values corresonding
	x = []; y = []
	for i in range(0, 8):
		x.append(nodeCoords[i][0])
		y.append(nodeCoords[i][1])

	#Included relative addition to remove potential of negative values(GUI does not
	#represent negative graph values)
	for i in range(0, 8):
		x[i] += 350
		y[i] += 350
		nodeCoords[i] = [x[i], y[i]]

	return nodeCoords
