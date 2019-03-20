import numpy, pandas, pickle, random, operator, sys, time
import matplotlib.pyplot as plt
from random import randint
from plotted import plotTSP
from CoordFromDistMatrix import getMatrixDomainCoords

bestRoute = []

#Class to define objects of nodes representing cities to be travelled.
#distance method allows for calculation of distance between self node
#and any given potential destination node by calculating x/y location
#variance. repr method shows distance calculated
class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def distance(self, node):
		dis_to_x = abs(self.x - node.x)
		dis_to_y = abs(self.y - node.y)
		dis_total = numpy.sqrt((dis_to_x ** 2) + (dis_to_y ** 2))
		return dis_total

	def __repr__(self):
		return str(self.x) + "," + str(self.y)

class Fitness:
	#Definition of the edge variables defining paths between nodes
	def __init__(self, route):
		self.route = route
		self.distance = 0
		#float val given to increase definition accuracy for close nodes
		self.fitness = 0.0

	#Defines the cost of a given Node to Node path for reference later
	def routeCost(self):
		if self.distance == 0:
			travelCost = 0
			for routes in range (0, len(self.route)):
				fromNode = self.route[routes]
				toNode = None
				if routes + 1 < len(self.route):
					toNode = self.route[routes + 1]
				else:
					toNode = self.route[0]
				travelCost += fromNode.distance(toNode)
			self.distance = travelCost
		return self.distance

	#Used to decide cost difference between possible paths. Lesser costs give a larger
	#number return. Big number is a better rank for of path cost
	def routeFitness(self):
		if self.fitness == 0:
			self.fitness = 1 / float(self.routeCost())
		return self.fitness

#Random selection of nodes in available node list for reference and analysis
def generateNode(nodeList):
	path = random.sample(nodeList, len(nodeList))
	return path

#Uses generateNode() above to generate the population to be referenced first.
def initialPopulation(size, nodeList):
	population = []
	for fullSize in range(0, size):
		population.append(generateNode(nodeList))
	return population

#Used to interface with the routeFitness method in the Node class to find path rankings
#generated in routeFitness()
def rankPaths(population):
	fitnessFindings = {}
	for item in range(0, len(population)):
		fitnessFindings[item] = Fitness(population[item]).routeFitness()
	return sorted(fitnessFindings.items(), key = operator.itemgetter(1), reverse = True)

#Selection of best paths is produced via an inclusion of random node
#selection for inspection, followed by verification of the node's
#potential against others through the implementation of elitism when
#selecting next generation parents
def selection(nodeRankings, eliteSize):
	selectionResults = []
	dataFrame = pandas.DataFrame(numpy.array(nodeRankings), columns=["Index","Fitness"])
	dataFrame['cum_sum'] = dataFrame.Fitness.cumsum()
	dataFrame['cum_perc'] = 100*dataFrame.cum_sum/dataFrame.Fitness.sum()
	for item in range(0, eliteSize):
		selectionResults.append(nodeRankings[item][0])
	for item in range(0, len(nodeRankings) - eliteSize):
		choice = 100*random.random()
		for item in range(0, len(nodeRankings)):
			if choice <= dataFrame.iat[i, 3]:
				selectionResults.append(nodeRankings[item][0])
				break
	return selectionResults

#Definition of most likely nodes to be selected for further
#generation development. Checks selection method to allow for
#inclusion of elite node choice based on route cost
def matingPool(population, selectionResults):
	matingPool = []
	for item in range(0, len(selectionResults)):
		index = selectionResults[item]
		matingPool.append(population[index])
	return matingPool

#Concrete choice method to allow for final definition of child
#node based on parents referenced in selection()->matingPool()
#these values are provided via the breedPopulation() method
#parameters below, and this method is called from within
def breed(parent1, parent2):
	child = []
	cParent1 = []
	cParent2 = []

	geneA = int(random.random() * len(parent1))
	geneB = int(random.random() * len(parent1))

	startGene = min(geneA, geneB)
	endGene = max(geneA, geneB)

	for i in range(startGene, endGene):
		cParent1.append(parent1[i])

	cParent2 = [item for item in parent2 if item not in cParent1]

	child = cParent1 + cParent2
	return child

#Dependent on the breed() method. All describe above
def breedPopulation(matingpool, eliteSize):
	children = []
	length = len(matingpool) - eliteSize
	pool = random.sample(matingpool, len(matingpool))

	for i in range(0,eliteSize):
		children.append(matingpool[i])

	for i in range(0, length):
		child = breed(pool[i], pool[len(matingpool)-i-1])
		children.append(child)
	return children

#Allows for deviation from qualification specification in case
#any optimal selection of child node was overlooked via the 
#selection and breeding methodology
def mutate(individual, mutationRate):
	for swapped in range(len(individual)):
		if(random.random() < mutationRate):
			swapWith = int(random.random() * len(individual))

			nodeOne = individual[swapped]
			nodeTwo = individual[swapWith]

			individual[swapped] = nodeTwo
			individual[swapWith] = nodeOne
	return individual

#Mechanism to call and properly define output of the mutate()
#method
def mutatePop(population, mutationRate):
	mutatedPop = []

	for ind in range(0, len(population)):
		mutatedInd = mutate(population[ind], mutationRate)
		mutatedPop.append(mutatedInd)
	return mutatedPop

#Activate method to allow for call to all predefined methods
#and thus apply GA through the mechanisms they define. Called
#more accurately for user input by the geneticAlgoritm() 
#method below which more astoutly defines user injestible
#output
def nextGeneration(currentGen, eliteSize, mutationRate):
	popRanked = rankPaths(currentGen)
	selectionResults = selection(popRanked, eliteSize)
	matingpool = matingPool(currentGen, selectionResults)
	children = breedPopulation(matingpool, eliteSize)
	nextGeneration = mutatePop(children, mutationRate)
	return nextGeneration

#Activate method to allow for call to all predefined methods
#and thus apply GA through the mechanisms they define
def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
	population = initialPopulation(popSize, population)
	initialPathCost = str(1 / rankPaths(population)[0][1])
	print("Initial Path Cost: " + initialPathCost + "km")

	newBest = str(1 / rankPaths(population)[0][1])	

	#Qualitatively search for best cost path
	for i in range(0, generations):
		population = nextGeneration(population, eliteSize, mutationRate)
		test = str(1 / rankPaths(population)[0][1])
		if test < newBest:
			newBest = test
		
	finalPathCost = newBest

	#Condition to guarantee later findings don't oppose initials for overall cost
	if initialPathCost < finalPathCost:
		print("Best Path Cost: " + initialPathCost + "km")
	else:
		print("Best Path Cost: " + finalPathCost + "km")

	bestRouteIndex = rankPaths(population)[0][0]
	global bestRoute
	bestRoute = population[bestRouteIndex]
	return bestRoute

#Definition of lists required for GUI representation
nodeList = []
printableNodeList = []
GivenNodeList = []

#Definition of the two domains to be tested in the assignment
#requirements document
Domain1 = [[20, 20], [20, 40], [60, 20], [100, 40], [160, 20], [200, 40], [180, 60], [120, 80], [140, 140], [180, 100], [200, 160], [180, 200], [140, 180], [100, 120], [100, 160], [80, 180], [60, 200], [20, 160], [40, 120], [60, 80]]
Domain2 = getMatrixDomainCoords()

#Used for GUI to further define the ordering of nodes to print
#This is implied by the GA analysis approach but is required
#for confirmation within the plotted.py script
pathDomain1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
pathDomain2 = [0, 1, 2, 3, 4, 5, 6, 7]

#Run the script as "python3 TSP.py 2" to run for domain2 in project requirements, otherwise
#domain1 will run
if sys.argv[1] == "2":
	Domain = Domain2
	pathDomain = pathDomain2
else:
	Domain = Domain1
	pathDomain = pathDomain1

#Used to convert GA findings to GUI readable format - change from
#Node objects to int values 
for i in range(0, len(Domain)):
	node = Node(Domain[i][0], Domain[i][1])
	GivenNodeList.append(node)

#True loop required to overcome indexing issues when GA negates
#nodes based on thru-definition call
while True:
	try:
		#call of GA to analyze from perspective of TSP
		test = geneticAlgorithm(population=GivenNodeList, popSize=100, eliteSize=int((sys.argv[3])), mutationRate=0.01, generations=int(sys.argv[2]))
		break
	except IndexError:
		print("INDEX ERROR from negated node")
		pass

#Used to convert GA findings to GUI readable format - change from
#Node objects to int values 
for i in range(0, len(Domain)):
	nodeInts = pickle.dumps(bestRoute[i])
	nodeInt = pickle.loads(nodeInts)
	printableNodeList.append([nodeInt.x, nodeInt.y])

#Used for dynamic argument selection of domain
thePaths = [pathDomain]

#Call the magic
plotTSP(thePaths, printableNodeList)
