#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:22:09 2019

@author: 3706539
"""

import random
import pylab
from matplotlib.pyplot import pause
import networkx as nx
pylab.ion()

graph = nx.Graph()
node_number = 0
graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))

def get_fig():
    global node_number
    node_number += 1
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    graph.add_edge(node_number, node_number-1)
    fig = pylab.figure()
    nx.draw(graph, pos=nx.get_node_attributes(graph,'Position'))
    return fig

num_plots = 10;
pylab.show()

for i in range(num_plots):

    fig = get_fig()
    fig.canvas.draw()
    pylab.draw()
    pause(2)
    pylab.close(fig)