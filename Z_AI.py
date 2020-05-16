import math
import pygame as pg
from pygame.locals import *
import random as rand
#hello

pg.init()

clock = pg.time.Clock()

gameDisplay = pg.display.set_mode((1280,720),pg.RESIZABLE)
gameDisplay.fill((0,0,0))

end = False

class Player:
	def __init__(self):
		self.x = int(1280/2)-2.5
		self.y= int(760/2)-2.5
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
class Zombie:
	def __init__(self):
		self.x = rand.randint(0,1280)
		self.y = rand.randint(0,760)
		self.xLen = 5
		self.yLen = 5
		self.color = (255,0,0)
		self.speed = 3
		self.drawR = None
		self.drawL = None
	def move(self,players,lwall):
		if(players.x-self.x != 0):
			angle = math.atan2(players.y-self.y,players.x-self.x)
		else:
			angle = 0
		self.drawL = pg.draw.line(gameDisplay,(255,0,0),(self.x,self.y),(players.x,players.y))
		temp = self.collide(self.drawL,lwall)
		if(temp != None):
			temp = temp[0]
			ec1 = pg.draw.line(gameDisplay,(0,0,0),(self.x,self.y),(temp.x-10,temp.y-10))
			ec2 = pg.draw.line(gameDisplay,(0,0,0),(self.x,self.y),(temp.x+temp.xLen+10,temp.y-10))
			ec3 = pg.draw.line(gameDisplay,(0,0,0),(self.x,self.y),(temp.x-10,temp.y+temp.yLen+10))
			ec4 = pg.draw.line(gameDisplay,(0,0,0),(self.x,self.y),(temp.x+temp.xLen+10,temp.y+temp.yLen+10))

			col1 = self.collide(ec1,lwall)
			col2 = self.collide(ec2,lwall)
			col3 = self.collide(ec3,lwall)
			col4 = self.collide(ec4,lwall)

			a1 = math.atan2(temp.y-10-self.y,temp.x-10-self.x)
			a2 = math.atan2(temp.y-10-self.y,(temp.x+temp.xLen+10)-self.x)
			a3 = math.atan2((temp.y+temp.yLen+10)-self.y,temp.x-10-self.x)
			a4 = math.atan2((temp.y+temp.yLen+10)-self.y,(temp.x+temp.xLen+10)-self.x)
			c1 = False
			c2 = False
			c3 = False
			c4 = False
			d1 = 100000
			d2 = 100000
			d3 = 100000
			d4 = 100000
			if(col1 == None):
				c11 = pg.draw.line(gameDisplay,(0,255,0),(temp.x-10,temp.y-10),(players.x,players.y))
				c1 = self.collide(c11,lwall)
				d1 = math.hypot(players.x-temp.x-10, players.y-temp.y-10)
			if(col2 == None):
				c22 = pg.draw.line(gameDisplay,(0,255,0),(temp.x+temp.xLen+10,temp.y-10),(players.x,players.y))
				c2 = self.collide(c22,lwall)
				d2 = math.hypot(players.x-(temp.x+temp.xLen+10), players.y-temp.y-10)
			if(col3 == None):
				c33 = pg.draw.line(gameDisplay,(0,255,0),(temp.x-10,temp.y+temp.yLen+10),(players.x,players.y))
				c3 = self.collide(c33,lwall)
				d3 = math.hypot(players.x-temp.x-10, players.y-(temp.y+temp.yLen+10))
			if(col4 == None):
				c44 = pg.draw.line(gameDisplay,(0,255,0),(temp.x+temp.xLen+10,temp.y+temp.yLen+10),(players.x,players.y))
				c4 = self.collide(c44,lwall)
				d4 = math.hypot(players.x-(temp.x+temp.xLen+10), players.y-(temp.y+temp.yLen+10))
			if(c1 != False):
				angle = a1
			if(c2 != False and d2<=d1):
				angle = a2
			if(c3 != False and d3<=d2 and d3<=d1):
				angle = a3
			if(c4 != False and d4<=d3 and d4<=d2 and d4<=d1):
				angle = a4
		#print(math.cos(angle))
		#print(math.sin(angle))
		self.x+=int(self.speed*math.cos(angle))
		self.y+=int(self.speed*math.sin(angle))
		self.drawR = pg.Rect(self.x-2.5,self.y-2.5,self.xLen,self.yLen)
		if(self.collide(self.drawR, lwall) != None):
			self.x-=int(self.speed*math.cos(angle))
			self.y-=int(self.speed*math.sin(angle))
	def draw(self):
		self.drawR = pg.draw.rect(gameDisplay,self.color,(self.x-2.5,self.y-2.5,self.xLen,self.yLen))
	def collide(self, rect, lwall):
		arr = []
		collide = False
		for i in lwall:
			if(i.drawR != None and rect.colliderect(i.drawR)):
				collide=True
				arr.append(i)
		if(len(arr) == 0):
			return None
		else:
			return arr


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

me = Player()
zombs = []
walls = []
for i in range(0,10):
	zombs.append(Zombie())
	walls.append(Walls())
while not end:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end = True
    gameDisplay.fill((0,0,0))
    keys = pg.key.get_pressed()
    me.move(keys)
    for i in range(0,10):
    	walls[i].draw()
    	zombs[i].draw()
    	zombs[i].move(me,walls)
    me.draw()
    pg.display.update()
    clock.tick(60)
pg.quit()
quit()
