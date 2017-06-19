import read, math, pygame
pygame.init()
pygame.font.init()

class General(object):
	"""Should probably be called the God class, for it's omniscience.  If not benevolence.""" 
	def __init__(self):
		self.mode = "start"
		self.data = read.read("data.txt")
		self.options = read.read("options.txt")
		self.map = 0 #where in maplist it is (index #)
		self.width = 640
		self.height = 480
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.arrowlist = []
		self.blocklist = []
		self.maplist = []
		self.furnishings = ["TABLE", "RAMP_R", "RAMP_L", "PULLEY", "ROPE", "TEXT", "RANDOM"]
		self.valid_block_tags = ["SIZE","FORCE","POS","COLOR"]
		self.wr = pygame.font.Font("freesansbold.ttf", 24)
		self.raws_write = pygame.font.Font("freesansbold.ttf", 16)
		self.message = 0
		self.in_a_click = False
		self.force_types = self.options["forces"]
		self.force_types_space = []
		self.force_types_space_filled = False
		self.tolerance = self.options["tolerance"]#10 degrees
		self.time_bomb = 0
		self.blocks_finished = 0
		self.win = False
		self.no_win_yet = ""
		self.interfacing_now = False
		self.home_buttons = []
		self.do_buttons_once = False
		self.white = self.options["color"]["SCENERY"]["MAP"]
		self.black = self.options["color"]["SCENERY"]["BACKGROUND"]
		self.keylist = [[pygame.K_a, "a"],[pygame.K_b, "b"],[pygame.K_c, "c"],[pygame.K_d, "d"],[pygame.K_e, "e"],[pygame.K_f, "f"],[pygame.K_g, "g"],[pygame.K_h, "h"],[pygame.K_i, "i"],[pygame.K_j, "j"],[pygame.K_k, "k"],[pygame.K_l, "l"],[pygame.K_m, "m"],[pygame.K_n, "n"],[pygame.K_o, "o"],[pygame.K_p, "p"],[pygame.K_q, "q"],[pygame.K_r, "r"],[pygame.K_s, "s"],[pygame.K_t, "t"],[pygame.K_u, "u"],[pygame.K_v, "v"],[pygame.K_w, "w"],[pygame.K_x, "x"],[pygame.K_y, "y"],[pygame.K_z, "z"]]

	def reset(self):
		self.mode = "start"
		self.map = 0
		self.width = 640
		self.height = 480
		self.blocklist = []
		self.arrowlist = []
		self.in_a_click = False
		self.message = 0
		self.time_bomb = 0
		self.blocks_finished = 0
		self.win = False
		self.interfacing_now = False
		self.home_buttons = []
		self.do_buttons_once = False

	def label_arrow(self, receipt):
		try:
			# print(receipt, "at an angle of", round(math.degrees(self.arrowlist[-1].angle), 1))
			self.arrowlist[-1].type = receipt
			self.arrowlist[-1].color = self.options["color"]["ARROW"]["SET"]
		except IndexError: pass

	def interface(self, clickpt):
		for trio in self.force_types_space:
			if clickpt[0] > trio[0][0] and clickpt[0] < trio[1][0]:
				if clickpt[1] > trio[0][1] and clickpt[1] < trio[1][1]:
					return trio[2]

	def check(self):
		#each block has blockname.forces = [(angle, name),(angle, name) ...]
		# print("arrowlist ",len(self.arrowlist), "\n\n")
		any_bad_arrows = False
		you_win = False
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
				any_bad_arrows = True
				arrow.color = self.options["color"]["ARROW"]["WRONG"]

		self.blocks_finished = 0
		for block in self.blocklist:
			# print("checking the blocks...", block.force_qty,"sep", block.arrow_qty, "sep",self.blocks_finished)
			if block.force_qty == block.arrow_qty:
				self.blocks_finished +=1
			if self.blocks_finished == len(self.blocklist):
				you_win = True
		self.time_bomb = self.options["timer"]
		if any_bad_arrows:
			you_win = False
			self.no_win_yet = "Bad arrows have been marked."
		else:
			if you_win == False:
				self.no_win_yet = "Not enough arrows. Keep going."
		if you_win:
			self.win = True

	def draw_message(self, lines, rect):
		pygame.draw.rect(self.screen, self.options["color"]["INTERFACE"]["POPUP_BKGD"], rect, 0)
		i=0; text_height = 16
		for line in lines:
			self.screen.blit(self.raws_write.render(line, True, self.options["color"]["INTERFACE"]["POPUP_TEXT"]), (64,64+(text_height*i)))
			i+=1

	def draw_words(self, text, pos):
		self.screen.blit(self.wr.render(text, True, self.white), pos)

	def draw_interface(self):
		pygame.draw.line(self.screen, self.white, (0,63),(640,63))
		self.draw_words("This is a(n) ____ force.", (0,0))
		pygame.draw.lines(self.screen, self.options["color"]["INTERFACE"]["CHECKMARK"], False,((600,40),(620,58),(640,0)),5)
		try: self.draw_words(str(round(math.degrees(self.arrowlist[-1].angle), 1))+"\u00B0",(0,64))
		except IndexError: pass	
		
		which = self.maplist[self.map].name
		self.draw_words(which, (self.width - self.wr.size(which)[0],64))
		
		x = self.wr.size("This is a(n) ____ force.")[0] + 6;y = 0
		for type in self.force_types:
			size = self.wr.size(type)
			length = size[0] + 10
			if x+length > 600:
				x = 0; y = 32
			self.draw_words(type, (x,y))
			pygame.draw.rect(self.screen,self.options["color"]["INTERFACE"]["BORDERS"],((x,y),size),1)
			if self.force_types_space_filled == False:
				self.force_types_space.append([(x,y), (x+size[0], y+size[1]), type])
				if len(self.force_types_space) >= len(self.force_types):
					self.force_types_space_filled = True
			x += length

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
		
	def draw_pulley(self, x, y, radius, color):
		pygame.draw.circle(self.screen, color, (x,y), radius)
	
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
			if brick.visible:
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
		for term in self.maplist:
			big = self.wr.size(term.name)
			rect = ((x-5,y-5), (big[0]+10, big[1]+10))
			pygame.draw.rect(self.screen, self.options["color"]["INTERFACE"]["INTRO_BUTTON_BKGD"], rect, 0)
			self.draw_words(term.name, (x,y))
			if y+40 > self.height:
				y = 40
				x = 10 + (self.width/2)
			else:
				y+=40
			if self.do_buttons_once == False:
				self.home_buttons.append((rect[0],(rect[0][0]+rect[1][0], rect[0][1]+rect[1][1]), term.name))
		self.do_buttons_once = True
	
	def carto_map(self):
		#go through the map, drawing the parts
		for i in self.maplist[self.map].partlist: #parts
			if i[0] == "TABLE":
				self.draw_table(int(i[1]), int(i[2]), int(i[3]), int(i[4]))
			elif i[0] == "RAMP_R":
				self.draw_ramp_r(int(i[1]), int(i[2]), int(i[3]))
			elif i[0] == "RAMP_L":
				self.draw_ramp_l(int(i[1]), int(i[2]), int(i[3]))
			elif i[0] == "PULLEY":
				if len(i) == 4:
					self.draw_pulley(int(i[1]), int(i[2]), int(i[3]), self.white)
				else:
					self.draw_pulley(int(i[1]), int(i[2]), int(i[3]), (int(i[4]), int(i[5]), int(i[6])))
			elif i[0] == "ROPE":
				self.draw_rope(i[1:])
			elif i[0] == "TEXT":
				self.draw_words_raws(i[1:])	
		
class Block(object):
	"""Block template, to be initialised for each block.  Objects are stored in General's blocklist"""
	def __init__(self, surface, data):
		#initialise variables
		self.x = 0
		self.y = 0
		self.tilt = 0
		self.sidelength = 0
		self.mass = 0
		self.color = (255,255,255)
		self.forces = []
		self.force_qty = 0
		self.arrow_qty = 0
		self.pointlist = []
		self.finished = False
		self.visible = True

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
			elif i[0] == "HIDE":
				self.visible = False
		self.force_qty = len(self.forces)

		half = int(self.sidelength/2)
		self.pointlist_orig = [(self.x+half,self.y-half), (self.x+half,self.y+half), (self.x-half,self.y+half), (self.x-half,self.y-half)]
		if self.tilt != 0:
			theta = -1 * math.radians(self.tilt)
			for i in self.pointlist_orig:
				x,y = i; 
				x -= self.x; y -= self.y; temp = []
				x_hold = int((x*math.cos(theta)) - (y*math.sin(theta)))
				y_hold =  int((x*math.sin(theta)) + (y*math.cos(theta))) 
				x_hold += self.x; y_hold += self.y
				temp.append(x_hold)
				temp.append(y_hold)
				self.pointlist.append(temp)
		else:
			self.pointlist = self.pointlist_orig

class Arrow(object):
	"""Make many of these Arrows, and store the resulting objects in General's arrowlist"""
	def __init__(self, surface, startpos):
		self.start = startpos
		self.end = startpos #will be modified later
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
class Map(object):
	"""A new attempt"""
	def __init__(self):
		self.partlist = []
		self.submaps = []
		self.name = ""
		self.data_start = 0
		self.data_stop = 0

	def update(self, c):
		self.partlist = self.submaps[c].partlist
		self.data_start = self.submaps[c].data_start
		self.data_stop = self.submaps[c].data_stop

class Message(object):
	def __init__(self, text):
		self.lines = []
		text = text + " "; wordlist = []; i=0; text_height = 16; width = 160; lengths = []; rounds = len(text); j=0; this_line = ""; runner = 0;
		self.sizing = pygame.font.Font("freesansbold.ttf", 16)
		while i < rounds:
			if text[i:i+1] == " ":
				wordlist.append(text[j:i]); j=i+1
			i+=1
		if len(wordlist) == 0: wordlist.append(text)
		
		for word in wordlist:
			lengths.append(self.sizing.size(word)[0])

		for l in lengths:
			if (runner + l + 3) > width:
				runner = 0
				self.lines.append(this_line)
				this_line = ""
			runner += (l+3)
			this_line = this_line + " " + wordlist[lengths.index(l)]
		self.lines.append(this_line)
		self.rect = ((60,60),(width+8,text_height*len(self.lines) + 8))


