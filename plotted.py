import matplotlib.pyplot as plt

def plotTSP(path, nodes):

    #path: Reduntant requirement. Path is implied as order provided by TSP.py (0, 1,...,24)
    #nodes: coordinates for the different nodes to be output

    # Unpack the primary TSP.py nodes in order and transform them to ordered coordinates
    x = []; y = []
    for i in path[0]:
        x.append(nodes[i][0])
        y.append(nodes[i][1])

    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads
    a_scale = float(max(x))/float(100)

    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale,
            color ='g', length_includes_head=True)
    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'g', length_includes_head = True)

    #Set axis too slightly larger than the set of x and y
    plt.xlim(0, max(x)*1.1)
    plt.ylim(0, max(y)*1.1)
    plt.show()
