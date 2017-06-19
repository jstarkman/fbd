#FBDs
import pygame, sys, math, classes, random
pygame.init()

g = classes.General() #warning, large amount of __init__ to do
g.clock = pygame.time.Clock()
pygame.display.set_caption("FBD practice")
pygame.display.set_icon(pygame.image.load("icon.bmp"))
g.window = pygame.display.set_mode((g.width, g.height))
g.screen = pygame.display.get_surface()

def cartographer(): #in form of tuples, but no other splits
	now_in = ""
	i = 0
	for tag in g.data:
		#g.maplist is where they should live
		if tag[0] == "MAP":
			if now_in == "submap":
				g.maplist[-1].submaps[-1].data_stop = i

			paper = classes.Map() #fill w/ data later
			g.maplist.append(paper)
			g.maplist[-1].name = tag[1]
			g.maplist[-1].data_start = i
			now_in = "map"
		elif tag[0] == "SUBMAP":
			if now_in == "submap":
				g.maplist[-1].submaps[-1].data_stop = i
		
			paper = classes.Map() #fill w/ data later
			g.maplist[-1].submaps.append(paper)
			g.maplist[-1].submaps[-1].data_start = i
			now_in = "submap"
		elif tag[0] in g.furnishings:
			if now_in == "map":
				g.maplist[-1].partlist.append(tag)
			elif now_in == "submap":
				g.maplist[-1].submaps[-1].partlist.append(tag)

		else: pass #is a block, or part of one
		i+=1
	#endings
	i = 0
	for term in g.maplist:
		try:
			term.data_stop = g.maplist[i+1].data_start
		except IndexError:
			term.data_stop = len(g.data)
		i+=1

def clicked_it(which):
	i=0
	for layout in g.maplist:
		if layout.name == which: #correct map chosen
			if layout.name == "Random":
				g.map = random.randint(1,len(g.maplist)-1)
			else:
				g.map = i
			if g.maplist[g.map].submaps != []:
				g.maplist[g.map].update(random.randint(0,len(g.maplist[g.map].submaps)-1))
			break
		i+=1
	g.mode = "mech"

	i = g.maplist[g.map].data_start; in_block = False; start_block = 0; end_block = 0;	
	#block inst time
	for tag in g.data[g.maplist[g.map].data_start:g.maplist[g.map].data_stop]: #start w/ map tag
		if tag[0] == "BLOCK":
			if in_block == True:
				in_block = False
				end_block = i
				holder = classes.Block(g.screen, g.data[start_block:end_block])
				g.blocklist.append(holder)
			start_block = i
			in_block = True
		i+=1
	holder = classes.Block(g.screen, g.data[start_block:g.maplist[g.map].data_stop])
	g.blocklist.append(holder)

		
def I(events):
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if g.mode == "mech":
				g.in_a_click = True
				if event.pos[1] < 64:
					g.interfacing_now = True
				else:
					newbie = classes.Arrow(g.screen, event.pos)
					newbie.color = g.options["color"]["ARROW"]["NEW"]
					g.arrowlist.append(newbie)

		elif event.type == pygame.MOUSEMOTION and g.in_a_click == True:
			#move arrowhead
			try:
				g.arrowlist[-1].end = event.pos
			except IndexError: pass

		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if g.mode == "mech":
				#stop the arrow
				g.in_a_click = False
				
				if g.interfacing_now == True:
					g.interfacing_now = False
					if event.pos[0] > 600:
						g.check()
					else:
						g.label_arrow(g.interface(event.pos))
			elif g.mode == "start":
				x,y = event.pos
				for button in g.home_buttons:
					if x > button[0][0] and x < button[1][0]:
						if y > button[0][1] and y < button[1][1]:
							clicked_it(button[2]);

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DELETE:
				try: 
					del g.arrowlist[-1]#kill the arrow.  Kill it!
				except IndexError: pass
			elif event.key == pygame.K_ESCAPE:
				if g.mode == "mech":
					g.mode = "start"
					g.reset()
				elif g.mode == "start":
					sys.exit()
			elif event.key == pygame.K_RETURN:
				if g.message == 0:
					g.check()
				else:
					g.message = 0
				
			else: #letter pressed
				for i in g.keylist:
					if event.key == i[0]:
						try: g.label_arrow(g.options["PFT"][i[1]])
						except KeyError: pass


def boom():
	if g.win == False:
		size = len(g.arrowlist)
		i=0
		while i < size:
			try:
				arrow = g.arrowlist[i]
				if arrow.good == False:
					#find it and kill it
					del g.arrowlist[i]
					print("Bad!")
				else:
					i+=1
			except IndexError:
				break
	else:
		print("Winner! \n")
		g.reset() #purge


def draw():
	g.screen.fill(g.black)
	if g.mode == "start":
		g.draw_home()
	elif g.mode == "mech":
		g.carto_map()
		g.draw_interface()
		g.draw_blocks()
		g.draw_arrows()
	if g.message != 0:
		g.draw_message(g.message.lines,g.message.rect)
	pygame.display.flip()


def main():
	cartographer();
	while True:
		I(pygame.event.get());

		if g.time_bomb !=0:
			if g.time_bomb == 1:
				boom();
			elif g.time_bomb == g.options["timer"]:
				if g.win:
					g.message = classes.Message("You have won. Good for you!")
				elif g.no_win_yet != "":
					g.message = classes.Message(g.no_win_yet)
			g.time_bomb -= 1		
		draw();
		g.clock.tick(30);

main();
pygame.quit();
sys.exit();