import numpy.random as nr
import numpy as np
import sys
from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx 
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import pygraphviz_layout

#For generation of latin squares
from sage.all import *
from sage.combinat.matrices.latin import *


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
	def __init__(self, n, disjoint=False,latin=False):
		self.people = []
		self.men_lists = []
		self.women_lists = []
		self.matching = [] #index:val = men:women
		self.cycles = [] # cycles in H(M)
		self.edges = [] # edges in H(M)
		self.n = n
		self.edges_populated = False
		self.cycles_populated = False
		self.disjoint=disjoint
		for x in range(n):
			self.people.append(x)
			self.matching.append(-1)
		if disjoint==False :
			# for x in self.people:
				# self.men_lists.append(nr.permutation(self.people).tolist())
				# self.women_lists.append(nr.permutation(self.people).tolist())
			self.men_lists = [  [0,1,2],
								[1,2,0],
								[2,0,1]]

			self.women_lists = [[1,2,0],
								[2,0,1],
								[0,1,2]]
		else:
			if not latin:
				mens_firsts = list(nr.permutation(self.people))
				womens_firsts = derangement(mens_firsts)
				#Now inverting the derangement
				womens_firsts = [womens_firsts.index(womens_firsts.index(i)) for i in womens_firsts]

				for i in self.people:
					self.men_lists.append([mens_firsts[i]]+nr.permutation(list(set(self.people)-{mens_firsts[i]})).tolist())
					self.women_lists.append([womens_firsts[i]]+nr.permutation(list(set(self.people)-{womens_firsts[i]})).tolist())
			else:
				# Generate a complete latin square uniformly at random
				gen = LatinSquare_generator(back_circulant(n))
				for i in range(20, 20+randint(1, 100)): next(gen)
				temp = next(gen).list()
				self.men_lists=[temp[i:i+n] for i in range(0,n*n,n)]

				for i in range(20, 20+randint(1, 100)): next(gen)
				temp = next(gen).list()
				self.women_lists=[temp[i:i+n] for i in range(0,n*n,n)]


	def printlists(self):
		print("\nMens List:\n")
		for i in range(self.n):
			print(i,"->",self.men_lists[i])

		print("\nWomens List:\n")
		for i in range(self.n):
			print(i,"->",self.women_lists[i])
		print()

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
		curr_m = deepcopy(self.matching)
		women_opt_m = deepcopy(Mz.matching)
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

		c =  deepcopy(self.cycles[cycle_no])
		c_pts =[]

		new_M = deepcopy(self)
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
	
	M = deepcopy(M_problem_instance)
	M.matching=[-1]*len(M.people)

	if optimal=="women":
		M.men_lists, M.women_lists = M.women_lists, M.men_lists
		
	unmatched = deepcopy(M.people)

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
	ll = deepcopy(lattice_levels)

	matching_vertex_dict[tuple(MO.matching)] = v
	vertex_level_dict[v]=0
	v=v+1

	# print( matching_vertex_dict[tuple(MO.matching)] )

	visited_vertices = set()
	visited_vertices.add(hash(tuple(MO.matching)))

	while lattice_levels:
		(M,l) = lattice_levels.pop(0)

		#if(M.matching==WO.matching):
			#print(l)
		M.findCycle(WO)
		for c in range(len(M.cycles)):

			if(tuple(M.cycles[c]) not in cycle_label_dict):

				tup = deepcopy(tuple(M.cycles[c]))
				#Adding all rotations of the  givem cycle, ex: (1,2,3),(2,3,1),(3,1,2)
				rot = list(tup)
				for i in tup:
					cycle_label_dict[tuple(rot)] = "ρ"+str(cycle_number)
					rot.append(rot.pop(0))
				cycle_number = cycle_number + 1

			# print(cycle_label_dict)

			Mc = M.removeCycle(WO,c)
			
			#To remove redudency, remove duplicates in the list
			if( hash(tuple(Mc.matching)) not in visited_vertices):
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


	# break_continue_matchings = break_all_continue_GS(MO,WO)#returns tuple of lists
	# color = [ matching_vertex_dict[tuple(i)] for i in break_continue_matchings ]
	# print("color: ",color,)

	#Now dwaring
	global no_fig
	G = nx.DiGraph()
	G.add_edges_from(lattice_edges)#,length=30,minlen=50)



	no_fig = no_fig+1
	fig = plt.figure(no_fig)
	fig.tight_layout()
	# plt.ion()
	pos = graphviz_layout(G,prog='dot')
	nx.draw_networkx(G, with_label=True,arrows=True,pos=pos,node_size=300,font_size=9,node_color='#ff5733')#ff5733 , cmap=plt.cm.Blues,node_color=range(len(G)),prog='dot'
	nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_cycle_dict,font_color='black',
		font_size=9,rotate=False,label_pos=0.6)
	# plt.show()

	# print(matching_vertex_dict)
	# print(vertex_level_dict)
	# print(lattice_edges)


	
	print("Total number of matchings: ",len(matching_vertex_dict))	
	

	for i in matching_vertex_dict:
		print("M"+str(matching_vertex_dict[i]),"->",i)

	print("Rotations: \n")
	label_cycle_dict = { v: k for k,v in cycle_label_dict.items()} #Inverting the dictionary
	for i in label_cycle_dict:
		print(i,"->",label_cycle_dict[i])

	#To make it tight_layout
	def on_resize(event):
		fig.tight_layout()
		fig.canvas.draw()

	cid = fig.canvas.mpl_connect('resize_event', on_resize)
	#Dont remove above code

	# print(cycle_label_dict)
	plt.show()	

def break_all_continue_GS(MO,WO):
	if MO.disjoint == False:
		return ()

	def break_first_propose(M):
		Mx = deepcopy(M)
		Mx.matching = [-1]*M.n
		#Mx is definatly disjoint, So everyone has seconf(m), no harm in deleting everyone's first
		for i in Mx.people:
			w = Mx.men_lists[i].pop(0)
			Mx.women_lists[w].pop()


		Nx = ext_gale_shaply(Mx,"men")
		print("printing Nx matching before sending:", Nx.matching)
		print("Nx lists")
		Nx.printlists()
		return Nx

	M1 = deepcopy(MO)
	break_continue_matchings=[M1]
	flag = True # If there is interesection with WO, set False
	
	while flag:
		M = break_first_propose(break_continue_matchings[-1])
		interesection_M_WO = [M.matching[i] for i in range(M.n) if M.matching[i]==WO.matching[i]]

		print(M.matching)
		print(WO.matching)
		print("intersection: ",interesection_M_WO)
		if ( len(interesection_M_WO) == 0 ): #If there is interesection, list will be non empty
			break_continue_matchings.append(M)
			M.disjoint = True
		else:
			flag = False

	print(len(break_continue_matchings))
	return tuple([I.matching for I in break_continue_matchings])

def random_derangement(n):
	while True:
		v = list(range(n))
		for j in range(n - 1, -1, -1):
			p = nr.randint(j+1)
			if v[p] == j:
				break
			else:
				v[j], v[p] = v[p], v[j]
		else:
			if v[0] != 0:
				return tuple(v)

def derangement(lst):
	nr = random_derangement(len(lst))
	dst = [lst[i] for i in nr]
	return dst				

def main():
	
	n = int(sys.argv[1])

	if(len(sys.argv) >= 3):
		seed = int(sys.argv[2])
	else:
		seed = nr.randint(100000000)
		print("seed1:",seed)

	nr.seed(seed)

	M = MarriageMatchingInstance(n,disjoint=False,latin=False)

	# M.printlists()
	# M.printlists()

	MO = ext_gale_shaply(M,"men")
	WO = ext_gale_shaply(M,"women")

	# # print("MO: ",MO.matching)
	# # print("WO: ",WO.matching)

	
	MO.findCycle(WO)
	WO.findCycle(WO)

# 	# # MO.printlists()

	drawLattice(MO,WO)
# 	# # break_all_continue_GS(MO,WO)

# ###################################
	# interesection_M_WO = [MO.matching[i] for i in range(MO.n) if MO.matching[i]==WO.matching[i]]
	# print(interesection_M_WO)
	# if interesection_M_WO:
	# 	pass
	# else:
	# 	print("Awesome")
	# 	MO.printlists()
	# 	for i in MO.people:
	# 		MO.men_lists[i].pop(0)
	# 		MO.women_lists[i].pop()
	# 	MO.matching = [-1]*MO.n
	# 	MO = ext_gale_shaply(MO,"men")
	# 	MO.printlists()

###########TESTING##################

###########TESTING##################

if __name__ == "__main__":
	main()