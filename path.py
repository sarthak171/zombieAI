import math
import pygame as pg
from pygame.locals import *
import random as rand


pg.init()

clock = pg.time.Clock()

gameDisplay = pg.display.set_mode((1280,720),pg.RESIZABLE)
gameDisplay.fill((0,0,0))

end = False

namenum = 0

#temp = line_rect((players.x,players.y),(self.x,self.y),lwall)
def line_rect(p1,p2,lwalls, rect):
	if(p2[0]-p1[0] != 0):
		m = float(p2[1]-p1[1])/float(p2[0]-p1[0])
	else:
		m = float(p2[1]-p1[1])/float(p2[0]-p1[0]+1)
	b = float(p2[1])-float(m*p2[0])
	for wall in lwalls:
		if((p1[0]>=wall.x and p2[0] <= wall.x) or (p2[0]>=wall.x and p1[0] <= wall.x)):
			init = wall.x
			while(init<=wall.x+wall.xLen):
				rect = pg.Rect(init-5,m*init+b-5,10,10)
				if(wall.drawR.colliderect(rect)):
					return True
				init+=2
	for i in lwalls:
		if(i.drawR.colliderect(rect)):
			return True
	return False
def line_rect1(p1,p2,lwalls):
	if(p2[0]-p1[0] != 0):
		m = float(p2[1]-p1[1])/float(p2[0]-p1[0])
	else:
		m = float(p2[1]-p1[1])/float(p2[0]-p1[0]+1)
	b = float(p2[1])-float(m*p2[0])
	for wall in lwalls:
		if((p1[0]>=wall.x and p2[0] <= wall.x) or (p2[0]>=wall.x and p1[0] <= wall.x)):
			init = wall.x
			while(init<=wall.x+wall.xLen):
				rect = pg.Rect(init-5,m*init+b-5,10,10)
				if(wall.drawR.colliderect(rect)):
					return True
				init+=2
	return False

class Player:
	def __init__(self):
		self.x = int(1280/2)
		self.y= int(760/2)
		self.xLen = 10
		self.yLen = 10
		self.color = (255,255,255)
		self.speed = 5
		self.drawR = None
	def move(self,keys):
		if keys[K_w]:
			self.y-=self.speed
		if(keys[K_s]):
			self.y+=self.speed     
		if(keys[K_d]):
			self.x+=self.speed       
		if(keys[K_a]):
			self.x-=self.speed
		if(self.x<=0 or self.x >=1280):
			self.x = 0
		if(self.y<=0 or self.y>=720):
			self.y = 0
	def draw(self):
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
class Walls:
	def __init__(self):
		self.x = rand.randint(100,1100)
		self.y = rand.randint(100,600)
		self.xLen = rand.randint(10,100)
		self.yLen = rand.randint(10,100)
		self.color = (0,0,255)
		self.drawR = None
	def draw(self):
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
class Graph:
	def __init__(self,nodes):
		self.edges = {}
		self.weights = {}
		self.start = None
		self.end = None
		global namenum
		for i in range(0,namenum+1):
			self.edges[str(i)]= []
			self.weights[str(i)]= []
		for node in nodes:
			for c in node.edges:
				self.edges[node.name].append(c[1].name)
				self.edges[c[1].name].append(node.name)
				self.weights[(node.name,c[1].name)] = math.hypot(c[1].x-node.x,c[1].y-node.y)
				self.weights[(c[1].name,node.name)] = math.hypot(c[1].x-node.x,c[1].y-node.y)
				if(c[1].start):
					self.start = c[1].name
					#pg.draw.circle(gameDisplay,(0,255,255),(self.start.x,self.start.y),5)
				if(c[1].end):
					self.end = c[1].name
					#pg.draw.circle(gameDisplay,(0,255,255),(self.end.x,self.end.y),5)
	def pathfinder(self):
		shortest_paths = {self.start: (None, 0)}
		current_node = self.start
		visited = set()
		while(current_node != self.end):
			visited.add(current_node)
			destinations = self.edges[current_node]
			weight_to_current_node = shortest_paths[current_node][1]
			for next_node in destinations:
				weight = self.weights[(current_node, next_node)] + weight_to_current_node
				if next_node not in shortest_paths:
					shortest_paths[next_node] = (current_node, weight)
				else:
					current_shortest_weight = shortest_paths[next_node][1]
					if current_shortest_weight > weight:
						shortest_paths[next_node] = (current_node, weight)
			next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
			current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
		path = []
		while current_node is not None:
			path.append(current_node)
			next_node = shortest_paths[current_node][0]
			current_node = next_node
		path = path[::-1]
		return path
class Zombie:
	def __init__(self):
		self.x = rand.randint(0,1280)
		self.y = rand.randint(0,760)
		self.xLen = 5
		self.yLen = 5
		self.color = (255,0,0)
		self.speed = 3
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
		self.drawL = None
	def move(self,players,lwall,nodes):
		if(players.x-self.x != 0):
			angle = math.atan2(players.y-self.y,players.x-self.x)
			m = (players.y-self.y)/(players.x-self.x)
		else:
			angle = 0
			m = (players.y-self.y)/.01
		l = pg.draw.line(gameDisplay,(255,0,0),(self.x,self.y),(players.x,players.y))
		temp = line_rect((players.x,players.y),(self.x,self.y),lwall,self.drawR)
		if(temp):
			print('Hi')
			self.addEdges(nodes,players,lwall)
			g = Graph(nodes)
			arr = g.pathfinder()
			minNode = nodes[0]
			minNodeD = 100000000
			if(len(arr) >= 3):
				dest = g.pathfinder()
				for node in nodes:
					for c in node.edges:
						if(minNodeD >= math.hypot(c[1].x-self.x,c[1].y-self.y) and math.hypot(c[1].x-self.x,c[1].y-self.y) != 0):
							minNode = c[1]
							minNodeD = math.hypot(c[1].x-self.x,c[1].y-self.y)
						for i in range(0,len(dest)):
							if(dest[i] == c[1].name):
								dest[i] = c[1]
								break
							if(dest[i] ==c[0].name):
								dest[i] = c[0]
								break
				ind = 0
				de = dest[1]
				dis = math.hypot(de.x-self.x,de.y-self.y)
				for d in dest:
					pg.draw.rect(gameDisplay,(0,255,255),(d.x,d.y,10,10))
				#if(minNode == de and math.hypot(dest[2].x-self.x,dest[2].y-self.y)<=100):
				#de = dest[2]
				'''
				while(ind+1 < len(dest) and dis<=math.hypot(dest[ind+1].x-self.x,dest[ind+1].y-self.y)):
					ind+=1
					de = dest[ind]
					dis = math.hypot(de.x-self.x,de.y-self.y)
				'''
				#print(minNodeD)
				pg.draw.rect(gameDisplay,(0,255,255),(de.x,de.y,10,10))
				angle = math.atan2(de.y-self.y,de.x-self.x)
		self.x+=int(self.speed*math.cos(angle))
		self.y+=int(self.speed*math.sin(angle))
		self.draw()
		if(self.collide(self.drawR, lwall)):
			self.x-=int(self.speed*math.cos(angle))
			self.y-=int(self.speed*math.sin(angle))
	def draw(self):
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
	def collide(self, rect, lwall):
		for i in lwall:
			if(i.drawR.colliderect(rect)):
				return True
		return False
	def addEdges(self,nodes,player,lwall):
		global namenum
		for node in nodes:
			if(not line_rect1((node.x,node.y),(player.x,player.y),lwall)):
				namenum+=1
				node.edges.append((node,Node(player.x,player.y,True,False,True,namenum)))
			if(not line_rect1((node.x,node.y),(self.x,self.y),lwall)):
				namenum+=1
				node.edges.append((node,Node(self.x,self.y,True,True,False,namenum)))				
def onePass(lwall):
	nodes = []
	biff = 23
	global namenum
	for wall in lwall:
		namenum+=1
		nodes.append(Node(wall.x-biff,wall.y-biff,False, False, False,namenum))
		namenum+=1
		nodes.append(Node(wall.x+wall.xLen+biff,wall.y-biff,False, False, False,namenum))
		namenum+=1
		nodes.append(Node(wall.x-biff,wall.y+wall.yLen+biff,False, False, False,namenum))
		namenum+=1
		nodes.append(Node(wall.x+wall.xLen+biff,wall.y+wall.yLen+biff,False, False, False,namenum))
	copy = nodes[:]
	for node in copy:
		for wall in lwall:
			if(wall.drawR.colliderect(node.drawR)):
				nodes.remove(node)
	return nodes
class Node:
	def __init__(self,x,y,v,s,e,name):
		self.x = x
		self.y= y
		self.xLen = 5
		self.yLen = 5
		self.color = (127,127,127)
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
		self.edges = []
		self.remove = v
		self.start = s
		self.end = e
		self.name = str(name)
	def draw(self,edgedraw):
		pg.draw.rect(gameDisplay,self.color,(self.x,self.y,self.xLen,self.yLen))
		if(edgedraw):
			for edge in self.edges:
				pg.draw.line(gameDisplay,(127,127,127),(self.x,self.y),(edge[1].x,edge[1].y))
def create_edges(nodes,lwall):
	for node in nodes:
		for c in nodes:
			collide = False
			temp = line_rect1((node.x,node.y),(c.x,c.y),lwall)
			if(not temp):
				node.edges.append((node,c))




me = Player()
zombs = []
walls = []
for i in range(0,1):
	zombs.append(Zombie())
	walls.append(Walls())
	walls[i].draw()
Nodes = onePass(walls)
create_edges(Nodes,walls)
while not end:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end = True
    gameDisplay.fill((0,0,0))
    keys = pg.key.get_pressed()
    me.move(keys)
    me.draw()
    for i in range(0,1):
    	walls[i].draw()
    	zombs[i].move(me,walls,Nodes)
    for node in Nodes:
    	node.draw(False)
    	for c in node.edges:
    		if(c[1].remove):
    			node.edges.remove(c)
    			namenum -=1
    pg.display.update()
    clock.tick(60)
pg.quit()
quit()