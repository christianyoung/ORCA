import networkx as nx
import matplotlib.pyplot as plt

def G_Draw(G):
	pos=nx.spring_layout(G)
	nx.draw(G,pos,node_size=50,node_color='#A0CBE2',alpha=0.5,edge_color='#BB0000',font_size=6)
	plt.show()
	
def Save(G,name):
	pos = nx.spring_layout(G,iterations=3)
	nx.draw(G,pos,node_size=50,node_color='#A0CBE2',alpha=0.5,edge_color='#BB0000',font_size=6)
	plt.savefig(name+'.png', dpi=300)
	plt.clf()
