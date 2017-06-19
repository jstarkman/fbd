#FBDs
import pygame, sys, math, classes
pygame.init()

g = classes.General() #warning, large amount of __init__ to do
g.clock = pygame.time.Clock()
pygame.display.set_caption("FBD practice")
pygame.display.set_icon(pygame.image.load("icon.bmp"))
g.window = pygame.display.set_mode((g.width, g.height))
g.screen = pygame.display.get_surface()

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
						receipt = g.interface(event.pos)
						try:
							print(receipt, "at an angle of", round(math.degrees(g.arrowlist[-1].angle), 1))
							g.arrowlist[-1].type = receipt
							g.arrowlist[-1].color = g.options["color"]["ARROW"]["SET"]
						except IndexError: pass
			elif g.mode == "start":
				x,y = event.pos
				for button in g.home_buttons:
					if x > button[0][0] and x < button[1][0]:
						if y > button[0][1] and y < button[1][1]:
							#clicked it
							for i in g.data: 
								if i[0] == button[2]: 
									g.map = i; break;
							g.mode = "mech"
							#inst blocks from their class
							block_data = g.blockify()
							for i in block_data:
								holder = classes.Block(g.screen, i)
								g.blocklist.append(holder)

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
				g.check()
			else: #letter pressed
				pass
				#if event.key == pygame.K_g:



def draw():
	g.screen.fill(g.black)
	if g.mode == "start":
		g.draw_home()
	elif g.mode == "mech":
		g.draw_map()
		g.draw_interface()
		g.draw_blocks()
		g.draw_arrows()
		
	pygame.display.flip()


def main():
	while True:
		I(pygame.event.get());
		if g.time_bomb !=0:
			if g.time_bomb == 1: #BOOM!
				if g.win == False:
					for arrow in g.arrowlist:
						if arrow.good == False:
							del g.arrowlist[g.arrowlist.index(arrow)]
							print("Bad!")
				else:
					print("Winner! \n")
					g.reset() #purge
					
			g.time_bomb -= 1
		draw()
		g.clock.tick(30)
main()
pygame.quit()
