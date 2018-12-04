import time
import pygame
import math as m
from pygame import gfxdraw
from pygame.locals import *

width = 1080
height = 720

pygame.init()
pygame.display.set_caption('Related Rates Simulation')
screen = pygame.display.set_mode([width, height])

class r:
	red = [230, 0, 0]
	dred = [200, 0, 0]
	white = [255, 255, 255]
	brown = [120, 65, 40]
	black = [20, 20, 20]
	yellow = [255, 255, 0]
	blue = [0, 20, 255]
	green = [0, 128, 0]
	dgreen = [0, 90, 0]
	orange = [255, 165, 0]
	purple = [128, 0, 128]

def draw_aaline(screen, p1, p2, thickness, color=r.white):
	length = m.hypot(p2[1] - p1[1], p2[0] - p1[0])
	center_L1 = ( (p1[0] + p2[0])/2, (p1[1] + p2[1])/2 )
	angle = m.atan2(p2[1] - p1[1], p2[0] - p1[0])
	UL = (center_L1[0] + (length / 2.) * m.cos(angle) - (thickness / 2.) * m.sin(angle),
		  center_L1[1] + (thickness / 2.) * m.cos(angle) + (length / 2.) * m.sin(angle))
	UR = (center_L1[0] - (length / 2.) * m.cos(angle) - (thickness / 2.) * m.sin(angle),
		  center_L1[1] + (thickness / 2.) * m.cos(angle) - (length / 2.) * m.sin(angle))
	BL = (center_L1[0] + (length / 2.) * m.cos(angle) + (thickness / 2.) * m.sin(angle),
		  center_L1[1] - (thickness / 2.) * m.cos(angle) + (length / 2.) * m.sin(angle))
	BR = (center_L1[0] - (length / 2.) * m.cos(angle) + (thickness / 2.) * m.sin(angle),
		  center_L1[1] - (thickness / 2.) * m.cos(angle) - (length / 2.) * m.sin(angle))

	pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)
	pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)

class Button:
	def __init__(self, pos, size, color, pressed_color=None):
		self.pos = pos
		self.size = size
		self.color = color
		self.pressed_color = pressed_color
		
	def is_pressed(self, m):
		return ((m[0] > self.pos[0]-self.size[0]/2)*(m[0] < self.pos[0]+self.size[0]/2)*
			   (m[1] > self.pos[1]-self.size[1]/2)*(m[1] < self.pos[1]+self.size[1]/2)*(pygame.mouse.get_pressed()[0]))
			   
	def draw(self):
		self.coords = ((self.pos[0]-self.size[0]/2,self.pos[1]-self.size[1]/2),(self.pos[0]+self.size[0]/2,self.pos[1]-self.size[1]/2),(self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2),(self.pos[0]-self.size[0]/2,self.pos[1]+self.size[1]/2))
		if self.is_pressed(pygame.mouse.get_pos()):
			pygame.gfxdraw.filled_polygon(screen, self.coords, self.pressed_color)
		else:
			pygame.gfxdraw.filled_polygon(screen, self.coords, self.color)
			
def capture_mouse(res):
	h = float('infinity')
	p1 = points[-1]
	p2 = mouse_pos
	dist = m.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2)
	if dist > res and not p2 in points:
		for point in points:
			if point[1] < h:
				h = point[1]
		if (p2[1] - p1[1]) < res:
			points.append((p2[0],((p2[1]<h)*p2[1])+((p2[1]>h)*h-.5)+((p2[1]==h)*h-.5)))

def draw_UI(pos):
	pygame.draw.line(screen, r.white, (pos[0]-200,height), (pos[0]-200,0),3)
	pygame.draw.line(screen, r.white, (pos[0]+200,height), (pos[0]+200,0),3)
	for i in range(len(points)):
		if i != 0:
			draw_aaline(screen, points[i], points[i-1], 3)
			draw_aaline(screen, ((pos[0]-points[i][0])+pos[0],points[i][1]), ((pos[0]-points[i-1][0])+pos[0],points[i-1][1]), 3)
	if len(points) != 1:
		draw_aaline(screen, points[0], ((pos[0]-points[0][0])+pos[0],points[0][1]), 2)
	
	pygame.draw.line(screen, r.white, (pos[0]+250,height), (pos[0]+250,0),3)
	pygame.draw.line(screen, r.white, (pos[0]+650,height), (pos[0]+650,0),3)
	
	
	
		
def fill_line(point_height_index, draw=False, top=False):
	status = 0
	c_point_height_index = points[0][1]-point_height_index
	middle = 400
	for point in points:
		if point[1] == c_point_height_index:
			if draw: pygame.draw.line(screen, r.blue, (point[0],c_point_height_index), (middle+(middle-point[0]),c_point_height_index),1)
			if not draw: return(middle-point[0])
			status = 1
			break # It's found, we're done here chief
	if status == 0:
		for i in range(len(points)-1):
			if points[i][1] > c_point_height_index and points[i+1][1] < c_point_height_index:
				b_bound = points[i]
				t_bound = points[i+1]
				if t_bound[0]-b_bound[0] != 0:
					slope = (t_bound[1] - b_bound[1]) / (t_bound[0] - b_bound[0])
					if draw: pygame.draw.line(screen, r.blue, (t_bound[0]+int((c_point_height_index-(t_bound[1]))/slope),(c_point_height_index-(t_bound[1]))+t_bound[1]), (middle+(middle-(t_bound[0]+int((c_point_height_index-(t_bound[1]))/slope))),c_point_height_index),1)
					if not draw: return(middle-(t_bound[0]+int((c_point_height_index-(t_bound[1]))/slope)))
					# for i in range(0,50): pygame.gfxdraw.pixel(screen, t_bound[0]+int(i/slope), int(i+t_bound[1]), r.red) # Slope lines
				else:
					if draw: pygame.draw.line(screen, r.blue, (points[i][0],c_point_height_index), (middle+(middle-points[i][0]),c_point_height_index),1)
					if not draw: return(middle-(points[i][0]))
				break
	if top: draw_aaline(screen, (400,c_point_height_index), (400+650,c_point_height_index),3)

points = [(0,0)]

button1  = Button((100,50), (100,50), r.green, r.dgreen)
last = False
switch = False

button2  = Button((100,125), (100,50), r.red, r.dred)
last2 = False
switch2 = False

h_ = 0
flag = 0
clock = pygame.time.Clock()
running = True
tick = 0
d_points = []
while running:
	clock.tick(30)
	screen.fill(r.black)
	draw_aaline(screen, (200,height), (600,height), 200, r.brown)
	
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()[0]
	
	if mouse_pressed:
		if flag == 0:
			flag = 1
			if (mouse_pos[0]>200)*(mouse_pos[0]<395):
				points = [mouse_pos]
				h_ = 0
				tick = 0
				switch = False
		if flag == 1:
			 if (mouse_pos[0]>200)*(mouse_pos[0]<395):
					capture_mouse(1)
	else: flag = 0

	if button1.is_pressed(mouse_pos) != last:
		last = button1.is_pressed(mouse_pos)
		if last:
			if switch:
				switch = False
				h_ = 0
				tick = 0
			else: switch = True
			
	if switch:
		dist = fill_line(h_)
		if h_ < points[0][1]-points[-1][1]:
			tick += 2
			h_ += .00001*(200 - dist)**2.5 + 2
			fill_line(int(h_), True, True)
			d_points.append([650+tick, points[0][1]-h_])
			
	if button2.is_pressed(mouse_pos):
		d_points = []
		# points = [[0,0]]
		tick = 0
		h_ = 0

	for i in range(len(d_points)):
		if i != 0:
			if d_points[i-1] < d_points[i]:
				draw_aaline(screen, d_points[i], d_points[i-1], 3, color=r.red)

	for i in range(0,int(h_)):
		if h_ > 1: fill_line(i,True)

	button1.draw()
	button2.draw()
	draw_UI((400,height/2))
	pygame.display.flip()
	# print mouse_pos
	# pygame.display.update()
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			running = False
			pygame.quit()
		if i.type == KEYDOWN:
			# pass
			if i.key == K_r:
				points = [mouse_pos]
				# h = float('infinity')
				d_points = []