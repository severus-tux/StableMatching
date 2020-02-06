import numpy.random as nr
import sys
import copy
import matplotlib.pyplot as plt
import networkx as nx 
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import pygraphviz_layout


no_fig=0

def dfs(u, marked, parent, adj):
	marked[u] = 1
	cycle = []
	for v in adj[u]:
		if marked[v] == 0:
			parent[v] = u
			cycle = dfs(v, marked, parent, adj) if cycle == [] else cycle
		elif marked[v] == 1:
			# cycle detected 
			new_cycle = []
			curr = u
			while curr != v:
				new_cycle.append(curr)
				curr = parent[curr]

			new_cycle.append(curr)
			cycle = new_cycle if cycle == [] else cycle

	marked[u] = 2
	return cycle

class MarriageMatchingInstance:
	def __init__(self, n):
		self.people = []
		self.men_lists = []
		self.women_lists = []
		self.matching = [] #index:val = men:women
		self.cycles = [] # cycles in H(M)
		self.edges = [] # edges in H(M)
		self.n = n
		self.edges_populated = False
		self.cycles_populated = False
		for x in range(n):
			self.people.append(x)
			self.matching.append(-1)
		for x in self.people:
			# self.men_lists.append(nr.permutation(self.people).tolist())
			# self.women_lists.append(nr.permutation(self.people).tolist())
			self.men_lists = [  [4,6,0,1,5,7,3,2],
								[1,2,6,4,3,0,7,5],
								[7,4,0,3,5,1,2,6],
								[2,1,6,3,0,5,7,4],
								[6,1,4,0,2,5,7,3],
								[0,5,6,4,7,3,1,2],
								[1,4,6,5,2,3,7,0],
								[2,7,3,4,6,1,5,0]]

			self.women_lists = [[4,2,6,5,0,1,7,3],
								[7,5,2,4,6,1,0,3],
								[0,4,5,1,3,7,6,2],
								[7,6,2,1,3,0,4,5],
								[5,3,6,2,7,0,1,4],
								[1,7,4,2,3,5,6,0],
								[6,4,1,0,7,5,3,2],
								[6,3,0,4,1,2,5,7]]
	
	def printlists(self):
		print("\nMens List:\n")
		for i in range(self.n):
			print(i,"->",self.men_lists[i])

		print("\nWomens List:\n")
		for i in range(self.n):
			print(i,"->",self.women_lists[i])

	def findCycle(self,Mz):
		self.cycles=[]
		if(self.edges_populated == False):
			self.populate_edges(Mz)

		edgeList = self.edges

		if(len(edgeList)==0):
			self.cycles=[]
			self.cycles_populated=True
			return

		n = 0
		for e in edgeList:
			n = max(n, max(e))

		n += 1
		adj = [list() for _ in range(n)]
		for e in edgeList:
			adj[e[0]].append(e[1])

		marked = [0] * n
		parent = [0] * n

		for start in range(n):
			if marked[start] == 0:
				c = dfs(start, marked, parent, adj)
				if c != []:
					self.cycles.append(c[::-1])

		self.cycles_populated=True
		return 

	def populate_edges(self,Mz):
		curr_m = copy.deepcopy(self.matching)
		women_opt_m = copy.deepcopy(Mz.matching)
		self.edges=[]

		for i in range(len(curr_m)): # i is man curr_m[i] is i's partner woman
			if(curr_m[i]!=women_opt_m[i]):
				Sm = self.men_lists[i][1]
				nextm = self.women_lists[Sm][-1]
				self.edges.append((i,nextm))
		

		self.edges_populated = True
		return 

		def draw_HM(self,Mz):
			if(self.edges_populated == False):
				self.populate_edges(Mz)
			if(self.cycles_populated == False):
				self.findCycle()

			G = nx.MultiDiGraph()
			G.add_edges_from(M.edges)
			global no_fig
			no_fig = no_fig+1
			#print(no_fig)
			plt.figure(no_fig)
			plt.ion()
			# pos = nx.spring_layout(G)
			nx.draw_networkx(G, with_label = True,connectionstyle='arc3, rad=0.2') #pos = nx.random_layout(G),
			plt.show()
			return


	def removeCycle(self,Mz, cycle_no=0):

		if (self.edges_populated == False):
			self.populate_edges(Mz)

		if(self.cycles_populated == False):
			self.findCycle()

		if len(self.cycles) == 0:
			return self
		if cycle_no>len(self.cycles) or cycle_no<0:
			print("\nNo such cycle!")
			return self

		c =  copy.deepcopy(self.cycles[cycle_no])
		c_pts =[]

		new_M = copy.deepcopy(self)
		new_M.cycles=[]
		new_M.edges=[]
		new_M.edges_populated=False
		new_M.cycles_populated=False
		
		for mi in c:
			wi=new_M.men_lists[mi].pop(0)
			c_pts.append(wi)
			wi1=new_M.men_lists[mi][0] #second will definately exist
			new_M.matching[mi]=wi1

		for wi in c_pts:
			while new_M.women_lists[wi][-1]!=new_M.matching.index(wi):
				m = new_M.women_lists[wi].pop(-1)
				if (wi in new_M.men_lists[m]):
					new_M.men_lists[m].remove(wi)
		return new_M		


def ext_gale_shaply(M_problem_instance,optimal="men"):
	
	M = copy.deepcopy(M_problem_instance)
	M.matching=[-1]*len(M.people)

	if optimal=="women":
		M.men_lists, M.women_lists = M.women_lists, M.men_lists
		
	unmatched = copy.deepcopy(M.people)

	while len(unmatched)>0:
		m = unmatched[0]
		unmatched.pop(0)
		w = M.men_lists[m][0] #w is the first women on m's list
		M.matching[m]=w #m proposes to the first women on his list

		last_man = M.women_lists[w][-1]

		if(M.matching[last_man] == w) and m!=last_man:
			M.matching[last_man] = -1
			unmatched.append(last_man)

		while(M.women_lists[w][-1]!=m):
			bad_m = M.women_lists[w][-1]
			M.men_lists[bad_m].remove(w)
			M.women_lists[w].remove(bad_m)

	if optimal=="women":
		M.men_lists, M.women_lists = M.women_lists, M.men_lists
		M.matching=[M.matching.index(M.matching.index(i)) for i in M.matching]

	return M

def drawLattice(MO,WO):
	MO.findCycle(WO)
	WO.findCycle(WO)

	v = 0 #vertex number
	cycle_number = 0 #cycle number
	vertex_level_dict = dict()  # int(v) -> int(l) level
	matching_vertex_dict = dict() # tuple(1,2,3) -> int(v)
	cycle_label_dict = dict() # [1,2,3] -> 1
	edge_cycle_dict = dict() # (1,2) -> "R1"
	lattice_edges = []

	lattice_levels = [] # (M,i) in lattice levets => M is in ith level of lattice
	lattice_levels.append((MO,0))
	ll = copy.deepcopy(lattice_levels)

	matching_vertex_dict[tuple(MO.matching)] = v
	vertex_level_dict[v]=0
	v=v+1

	# print( matching_vertex_dict[tuple(MO.matching)] )

	while lattice_levels:
		(M,l) = lattice_levels.pop(0)

		#if(M.matching==WO.matching):
			#print(l)
		M.findCycle(WO)
		for c in range(len(M.cycles)):

			if(tuple(M.cycles[c]) not in cycle_label_dict):

				tup = copy.deepcopy(tuple(M.cycles[c]))
				#Adding all rotations of the  givem cycle, ex: (1,2,3),(2,3,1),(3,1,2)
				rot = list(tup)
				for i in tup:
					cycle_label_dict[tuple(rot)] = "ρ"+str(cycle_number)
					rot.append(rot.pop(0))
				cycle_number = cycle_number + 1

			# print(cycle_label_dict)

			Mc = M.removeCycle(WO,c)
			
			#To remove redudency, remove duplicates in the list
			if(len(lattice_levels)==0):
				lattice_levels.append((Mc,l+1))
				ll.append((Mc,l+1))
			else:
				if((lattice_levels[-1][0].matching,lattice_levels[-1][1]) != (Mc.matching,l+1)): #Dont compare Objects, They would be two different copies of the same matchings
					lattice_levels.append((Mc,l+1))
					ll.append((Mc,l+1))

			if tuple(Mc.matching) not in matching_vertex_dict:
				matching_vertex_dict[tuple(Mc.matching)] = v
				vertex_level_dict[v]=l+1
				v=v+1
			
			parent = matching_vertex_dict[tuple(M.matching)]
			child = matching_vertex_dict[tuple(Mc.matching)]

			lattice_edges.append((parent,child))
			edge_cycle_dict[(parent,child)] = cycle_label_dict[tuple(M.cycles[c])]

	#Now dwaring
	global no_fig
	G = nx.DiGraph()
	G.add_edges_from(lattice_edges)
	no_fig = no_fig+1
	plt.figure(no_fig)
	# # plt.ion()			# self.men_lists.append(nr.permutation(self.people).tolist())
			# self.women_lists.append(nr.permutation(self.people).tolist())

	# # pos = nx.spring_layout(G)
	# nx.draw_networkx(G, with_label = True)#,connectionstyle='arc3, rad=0.2') #pos = nx.random_layout(G),

	# nx.draw(G, pos=graphviz_layout(G), node_size=1600, cmap=plt.cm.Blues,
 #        node_color=range(len(G)),
 #        prog='dot')
	pos = pygraphviz_layout(G,prog='dot')
	nx.draw_networkx(G, with_label=True,arrows=True,pos=pos,node_size=500,node_color='#ff5733')# , cmap=plt.cm.Blues,node_color=range(len(G)),prog='dot'
	nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_cycle_dict,font_color='black',label_pos=0.5)
	# plt.show()

	# print(matching_vertex_dict)
	# print(vertex_level_dict)
	# print(lattice_edges)


	
	print("Total number of matchings: ",len(matching_vertex_dict))	
	

	for i in matching_vertex_dict:
		print(matching_vertex_dict[i],"->",i)


	# print(cycle_label_dict)
	plt.show()	


def main():
	
	n = int(sys.argv[1])

	if(len(sys.argv) == 3):
		seed = int(sys.argv[2])
	else:
		seed = nr.randint(100000000)
		print("seed:",seed)

	nr.seed(seed)

	M = MarriageMatchingInstance(n)
	MO = ext_gale_shaply(M,"men")
	WO = ext_gale_shaply(M,"women")

	print("MO: ",MO.matching)
	print("WO: ",WO.matching)
	
	MO.findCycle(WO)
	WO.findCycle(WO)


	drawLattice(MO,WO)

	# lattice_levels = [] # (M,i) in lattice levets => M is in ith level of lattice
	# lattice_levels.append((MO,0))
	# ll = copy.deepcopy(lattice_levels)

	# while lattice_levels:
	# 	(M,l) = lattice_levels.pop(0)
	# 	if(M.matching==WO.matching):
	# 		print(l)
	# 	M.findCycle(WO)
	# 	for c in range(len(M.cycles)):
	# 		Mc = M.removeCycle(WO,c)
	# 		lattice_levels.append((Mc,l+1))
	# 		ll.append((Mc,l+1))

	# lattice_levels = ll
	# Mu = {x[0] for x in lattice_levels}
	# Mu_matching = {tuple(x.matching) for x in Mu}
	# print("Total number of matchings: ",len(Mu_matching))

	# ################del#############
	# mt = [[x for x in list(i)] for i in Mu_matching]
	# print(*mt,sep="\n")
	# ################del#############

if __name__ == "__main__":
    main()