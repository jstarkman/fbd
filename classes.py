import read, math, pygame
pygame.init()
pygame.font.init()
#screen.blit(writing.render("", True, color), (x,y))

class General(object):
	"""Should probably be called the God class, for it's omniscience.  If not benevolence.""" 
	def __init__(self):
		self.mode = "start"
		self.data = read.read("data.txt")
		self.options = read.read("options.txt")
		self.mapchoice = 0
		self.map = []
		self.width = 640
		self.height = 480
		self.center = (self.width/2, self.height/2)
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.blocklist = []
		self.arrowlist = []
		self.in_a_click = False
		self.wr = pygame.font.Font(None, 32)
		self.raws_write = pygame.font.Font(None, 24)
		self.force_types = ["frictional","gravitational","normal","natural","tensional","personal","inertial"]
		self.force_types_space = []
		self.force_types_space_filled = False
		self.tolerance = self.options["tolerance"]#10 degrees
		self.time_bomb = 0
		self.blocks_finished = 0
		self.win = False
		self.interfacing_now = False
		self.home_buttons = []
		self.do_buttons_once = False
		self.white = self.options["color"]["SCENERY"]["MAP"]
		self.black = self.options["color"]["SCENERY"]["BACKGROUND"]
		
	def reset(self):
		self.mode = "start"
		self.mapchoice = 0
		self.map = []
		self.width = 640
		self.height = 480
		self.center = (self.width/2, self.height/2)
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.blocklist = []
		self.arrowlist = []
		self.in_a_click = False
		self.force_types = ["frictional","gravitational","normal","natural","tensional","personal","inertial"]
		self.force_types_space = []
		self.force_types_space_filled = False
		self.tolerance = self.options["tolerance"]#10 degrees
		self.time_bomb = 0
		self.blocks_finished = 0
		self.win = False
		self.interfacing_now = False
		self.home_buttons = []
		self.do_buttons_once = False
	
	def interface(self, clickpt):
		for trio in self.force_types_space:
			if clickpt[0] > trio[0][0] and clickpt[0] < trio[1][0]:
				if clickpt[1] > trio[0][1] and clickpt[1] < trio[1][1]:
					return trio[2]
	
	def check(self):
		#each block has blockname.forces = [(angle, name),(angle, name) ...]
		# print("arrowlist ",len(self.arrowlist), "\n\n")
		
		for arrow in self.arrowlist:
			# print("named",arrow.type)
			for block in self.blocklist:
				x = arrow.start[0] - block.x; y = arrow.start[1] - block.y
				if int(math.sqrt((x*x) + (y*y))) < int(block.sidelength * 363 / 512):
					arrow.attached = self.blocklist.index(block) #tells what place in the lineup the attached block is
			if arrow.attached >= 0:
				for force in self.blocklist[arrow.attached].forces:
					# print(int(math.degrees(arrow.angle)),"more numbers",force[1])
					# print(arrow.type, "typical", force[0])
					if arrow.type == force[0]:
						#is it close?
						if math.degrees(arrow.angle) > (360-self.tolerance):
							arrow.angle -= (2*math.pi)
						if abs(int(math.degrees(arrow.angle)) - force[1]) < self.tolerance:
							if arrow.good != True:
								arrow.good = True
								self.blocklist[arrow.attached].arrow_qty +=1
			if arrow.good == True:
				arrow.color = self.options["color"]["ARROW"]["RIGHT"]
			else:
				arrow.color = self.options["color"]["ARROW"]["WRONG"]

		self.blocks_finished = 0
		for block in self.blocklist:
			# print("checking the blocks...", block.force_qty,"sep", block.arrow_qty, "sep",self.blocks_finished)
			if block.force_qty == block.arrow_qty:
				self.blocks_finished +=1
			if self.blocks_finished == len(self.blocklist):
				self.win = True
		self.time_bomb = 30

	def draw_words(self, text, pos):
		self.screen.blit(self.wr.render(text, True, self.white), pos)

	def draw_interface(self):
		pygame.draw.line(self.screen, self.white, (0,63),(640,63))
		self.draw_words("This is a(n) ____ force.", (0,0))
		pygame.draw.lines(self.screen, self.options["color"]["INTERFACE"]["CHECKMARK"], False,((600,40),(620,58),(640,0)),5)
		
		x = 250;y = 0
		for type in self.force_types:
			size = self.wr.size(type)
			length = size[0] + 10
			if x+length > 560:
				x = 0; y = 32
			self.draw_words(type, (x,y))
			pygame.draw.rect(self.screen,self.options["color"]["INTERFACE"]["BORDERS"],((x,y),size),1)
			if self.force_types_space_filled == False:
				self.force_types_space.append([(x,y), (x+size[0], y+size[1]), type])
				if len(self.force_types_space) >= len(self.force_types):
					self.force_types_space_filled = True
			x += length
	
	def blockify(self):
		data = []
		for i in self.map[2]: #blocks - each i is a new block (or the blank)
			try:
				if i[0] != "b" :#and i[0] != []:
					data.append(i)
				else:
					pass
			except IndexError:
				pass
		return data

	def draw_table(self, a,b,c,d):
		rect = ((a,b),(c,d)) #a,b for upper left xy, c,d for widthheight
		pygame.draw.rect(self.screen, self.white, rect)
	
	def draw_ramp_r(self, incline, x, y):
		point_list = [(x,y), (x,479)]
		height = 479-y
		trig = math.tan(math.radians(incline))
		width = int(height/trig)
		if x > width:
			#hits floor
			point_list.append((x-width,479))
		else:
			#hits wall
			Y = y + (x * trig)
			point_list.append((0,479))
			point_list.append((0,Y))
		
		pygame.draw.polygon(self.screen, self.white, point_list)

	def draw_ramp_l(self, incline, x, y):
		point_list = [(x,y), (x,479)]
		height = 479-y
		trig = math.tan(math.radians(incline))
		width = -1 * int(height/trig)
		if self.width - x > width:
			#hits floor
			point_list.append((x+width,479))
		else:
			#hits wall
			point_list.append((x+width,479))
			# Y = 479 - (639-x)*trig
			# point_list.append((639,479))
			# point_list.append((639,Y))
		
		pygame.draw.polygon(self.screen, self.white, point_list)
		
	def draw_pulley(self, x, y, radius):
		pygame.draw.circle(self.screen, self.white, (x,y), radius)
	
	def draw_rope(self, data): #data is [] of stringy ints
		j=0
		for num in data:
			data[j] = int(num)
			j+=1

		pts = []
		i = len(data)
		while i !=0:
			i-=2 #yes, it draws it backwards.  You're very clever.
			pts.append((data[i], data[i+1]))
		pygame.draw.lines(self.screen, self.options["color"]["SCENERY"]["ROPE"], 0, pts, 3)

	def draw_map(self): #map is a [ [] [] [] [] [] [] etc] 
		#this draws the scenery - tables, ramps, pulleys
		for i in self.map[1]: #parts
			if i[0] == "TABLE":
				self.draw_table(int(i[1]), int(i[2]), int(i[3]), int(i[4]))
			elif i[0] == "RAMP_R":
				self.draw_ramp_r(int(i[1]), int(i[2]), int(i[3]))
			elif i[0] == "RAMP_L":
				self.draw_ramp_l(int(i[1]), int(i[2]), int(i[3]))
			elif i[0] == "PULLEY":
				self.draw_pulley(int(i[1]), int(i[2]), int(i[3]))
			elif i[0] == "ROPE":
				self.draw_rope(i[1:])
			elif i[0] == "TEXT":
				self.draw_words_raws(i[1:])
			
	def draw_words_raws(self, data):
		#data is [text, x,y,R,G,B]
		j = 1
		for num in data[1:]:
			data[j] = int(num)
			j+=1
		self.screen.blit(self.raws_write.render(data[0], True, (data[3], data[4], data[5])), (data[1], data[2]))
		
	def draw_blocks(self):
		#draws all of the blocks.  Loops.
		for brick in self.blocklist:
			pygame.draw.polygon(self.screen, brick.color, brick.pointlist)
	
	def draw_arrows(self):
		for bolt in self.arrowlist:
			pygame.draw.line(self.screen, bolt.color, bolt.start, bolt.end, 3)
			bolt.find_head()
			pygame.draw.polygon(self.screen, bolt.color, bolt.headpts)
	
	def draw_home(self):
		text = "Free Body Diagrams practice"
		self.draw_words(text, ((self.width - self.wr.size(text)[0])/2,0))
		x = 10
		y = 40
		for map in self.data:
			big = self.wr.size(map[0])
			rect = ((x-5,y-5), (big[0]+10, big[1]+10))
			pygame.draw.rect(self.screen, (128,0,0), rect, 0)
			self.draw_words(map[0], (x,y))
			if y+40 > self.height:
				y = 50
				x = 10 + (self.width/2)
			else:
				y+=40
			if self.do_buttons_once == False:
				self.home_buttons.append((rect[0],(rect[0][0]+rect[1][0], rect[0][1]+rect[1][1]), map[0]))
		self.do_buttons_once = True

class Block(object):
	"""Block template, to be initialised for each block.  Objects are stored in General's blocklist"""
	def __init__(self, surface, data):
		#initialise variables
		self.x = 0
		self.y = 0
		self.tilt = 0
		self.sidelength = 0
		self.mass = 0
		self.color = (0,0,0)
		self.forces = []
		self.force_qty = 0
		self.arrow_qty = 0
		self.pointlist = []
		self.finished = False
		
		for i in data: #eg [size, 50, 25]
			if i[0] == "SIZE":
				self.sidelength = int(i[1])
				self.mass = int(i[2])
			elif i[0] == "FORCE":
				self.forces.append((i[1], int(i[2])))
			elif i[0] == "POS":
				self.x = int(i[1])
				self.y = int(i[2])
				self.tilt = int(i[3])
			elif i[0] == "COLOR":
				self.color = (int(i[1]), int(i[2]), int(i[3]))
		
		self.force_qty = len(self.forces)
		#pointlist - dx&y were calculated for one corner.  Law of cosines.
		dy=0; dx=0; theta=0;
		if self.tilt != 0:
			theta = math.cos(math.radians(self.tilt))
			dx = int(self.sidelength * theta * math.sqrt(1-theta))
			dy = int(self.sidelength * math.sin(math.radians(self.tilt)) * math.sqrt(1-theta))
		halfa = int(self.sidelength/2)
		self.pointlist = [(self.x+halfa-dx,self.y-halfa-dy), (self.x+halfa+dy,self.y+halfa-dx), (self.x-halfa+dx,self.y+halfa+dy), (self.x-halfa-dy,self.y-halfa+dx)]

class Arrow(object):
	"""Make many of these Arrows, and store the resulting objects in General's arrowlist"""
	def __init__(self, surface, startpos):
		self.start = startpos
		self.end = (1,1)
		self.angle = 0
		self.headpts = []
		self.color = (0,0,0)
		self.type = ""
		self.attached = -1
		self.good = False

	def find_head(self): #geometry!
		self.headpts = [self.end]
		
		half_pi = math.pi / 2
		if self.end[0] > self.start[0]:
			#I or IV
			if self.end[1] > self.start[1]:
				self.angle = math.atan((self.start[1]-self.end[1])/(self.end[0]-self.start[0]))
				self.angle += (4*half_pi)
			elif self.end[1] < self.start[1]:
				self.angle = math.atan((self.start[1]-self.end[1])/(self.end[0]-self.start[0]))
			else:
				self.angle = 0
		elif self.end[0] < self.start[0]:
			#II or III
			if self.end[1] > self.start[1]:
				self.angle = math.atan((self.start[1]-self.end[1])/(self.end[0]-self.start[0]))
				self.angle += (2*half_pi)
			elif self.end[1] < self.start[1]:
				self.angle = math.atan((self.start[1]-self.end[1])/(self.end[0]-self.start[0]))
				self.angle += (2*half_pi)
			else:
				self.angle = (2*half_pi)
		else:
			#vertical
			if self.end[1] > self.start[1]:
				self.angle = (3*half_pi)
			elif self.end[1] < self.start[1]:
				self.angle = (1*half_pi)
			else:
				#no arrow
				pass
		
		mdx = 10 * math.cos(self.angle)
		mdy = 10 * math.sin(self.angle)
		midpt = (self.end[0] - mdx, self.end[1] + mdy)
		dy = mdx
		dx = mdy
		self.headpts.append((midpt[0]+dx, midpt[1]+dy))
		self.headpts.append((midpt[0]-dx, midpt[1]-dy))
		#self.headpts has been updated.  No need to return anything.

