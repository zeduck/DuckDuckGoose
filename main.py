import pygame
import time
import random

pygame.init() 

width = 640
height = 480
backgroundcolour = (110, 255, 255)  #(red,green,blue) range from 0 to 255

screen = pygame.display.set_mode((width,height))

font = pygame.font.SysFont("comicsansms", 30)

#music
# pygame.mixer.init() 
# pygame.mixer.music.load('song.ogg')
# pygame.mixer.music.set_volume(0.2) #change
# pygame.mixer.music.play()

#grass
grass = pygame.Rect(0, height-25, width, 25)

#duck stats
#[xpos, ypos, xvel, yvel, yacc, jumpvel] 
duck = [160,300,4.5,0,0.075,-4] 	#duck[2] is movement speed, duck[4] is fall speed, duck[5] is jump height
duckpicture = pygame.image.load("./duck.jpg")
duckpicture = pygame.transform.scale(duckpicture, (41, 54))
duckrect = duckpicture.get_rect()
duckhit = 0

#goose stats
goose = [439,300,3.5,0,0.2,-8] #goose[2] is movement speed, goose[4] is fall speed, goose[5] is jump height
goosepicture = pygame.image.load("./goose.jpg")
goosepicture = pygame.transform.scale(goosepicture, (41,54))
gooserect = goosepicture.get_rect()
goosehit = 0

#egg
eggpicture = pygame.image.load("./egg.jpg")
eggpicture = pygame.transform.scale(eggpicture, (20,20))
eggrect = eggpicture.get_rect()

#obstacles
	#lemonde stand
standpicture = pygame.image.load("./stand.png")
standpicture = pygame.transform.scale(standpicture, (90,100))
standrect = standpicture.get_rect()

	#goose well
wellpicture = pygame.image.load("./well.png")
wellpicture = pygame.transform.scale(wellpicture, (90,100))
wellrect = wellpicture.get_rect()

#boost pad
boostpicture = pygame.image.load("./LaunchPad.png")
boostpicture = pygame.transform.scale(boostpicture,(100,60))
boostrect = boostpicture.get_rect()

#egg functions
eggs = []

def createegg(eggs):
	eggs.append([random.randrange(5, width-25), 5, 0, 0, 0.1]) #xinitpos, yinitpos, xvel, yvel, yacc
	#eggs[x][4] is fall speed

def drawegg(eggs):
	for egg in eggs:
		eggrect.x = egg[0]
		eggrect.y = egg[1]
		screen.blit(eggpicture, eggrect)
	for egg in eggs:
		egg[1] += egg[3] 
		egg[3] += egg[4]
		if (egg[1] + 20) >= (height-25):
			eggs.remove(egg)

def eggcatch(eggs, duckrect, gooserect):
	global duckhit, goosehit
	for egg in eggs:
		#left side of circle or the right side of the circle is between the left and right sides of the rect
		#top side of circle or the bottom side of the circle is between the top and bottom sides of the rect
		if (duckrect.x <= egg[0] <= duckrect.x + 41 or duckrect.x <= egg[0] + 20 <= duckrect.x + 41) and (duckrect.y <= egg[1] <= duckrect.y + 54 or duckrect.y <= egg[1] + 20 <= duckrect.y + 54):
			eggs.remove(egg)
			duckhit += 1
		elif (gooserect.x <= egg[0] <= gooserect.x + 41 or gooserect.x <= egg[0] + 20 <= gooserect.x + 41) and (gooserect.y <= egg[1] <= gooserect.y + 54 or gooserect.y <= egg[1] + 20 <= gooserect.y + 54):
			eggs.remove(egg)
			goosehit += 1

def boostpad(boostrect, duckrect, gooserect):
	global duck, goose
	
	if (duckrect.left <= boostrect.right and duckrect.right >= boostrect.left) and duckrect.bottom >= boostrect.top:
		duck[3] = duck[5] - 1	#boost height
		duck[1] += duck[3] 
	if (gooserect.left <= boostrect.right and gooserect.right >= boostrect.left) and gooserect.bottom >= boostrect.top:
		goose[3] = goose[5] - 2	#boost height
		goose[1] += goose[3] 

#length of a round
seconds = 60 #default 60 + 15

startingscreen = True

while True:
  
	if startingscreen == True: #starting screen
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					startingscreen = False

		screen.fill((124, 235, 185))

		font = pygame.font.SysFont("timesnewroman", 70)
		screen.blit(font.render("duck duck goose", True, (0,0,0)), (20, 15))
		pygame.draw.line(screen, (0,0,0), (30,100),(width-30, 100), 3)
		
		font = pygame.font.SysFont("comicsansms", 30)
		screen.blit(font.render("Instructions:", True, (0,0,0)), (50, 150))
		screen.blit(font.render("Move your character and", True, (0,0,0)), (50, 200))
		screen.blit(font.render("touch more eggs than", True, (0,0,0)), (50, 230))
		screen.blit(font.render("your opponent to win.", True, (0,0,0)), (50,260))
		screen.blit(font.render("The duck runs faster and", True, (0,0,0)), (50,290))
		screen.blit(font.render("the goose jumps higher", True, (0,0,0)), (50,320))
		screen.blit(font.render("Movement:", True, (0,0,0)), (400, 150))

		font = pygame.font.SysFont("ariel", 60)
		screen.blit(font.render("press space to start", True, (0,0,0)), (120,400))

		arrowkeyrect = pygame.transform.scale(pygame.image.load("arrowkeys.png"), (100, 100)).get_rect()
		arrowkeyrect.x = 480
		arrowkeyrect.y = 180
		screen.blit(pygame.transform.scale(pygame.image.load("arrowkeys.png"), (100, 100)), arrowkeyrect)

		wasdkeyrect = pygame.transform.scale(pygame.image.load("wasdkeys.png"), (90, 60)).get_rect()
		wasdkeyrect.x = 485
		wasdkeyrect.y = 300
		screen.blit(pygame.transform.scale(pygame.image.load("wasdkeys.png"), (90, 60)), wasdkeyrect)

		gooserect.x = 410
		gooserect.y = 200
		screen.blit(goosepicture,gooserect)

		duckrect.x = 410
		duckrect.y = 300
		screen.blit(duckpicture,duckrect)

		font = pygame.font.SysFont("comicsansms", 30)

	elif seconds <= 60 and seconds >= 0: #game starts

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_w:
					if (480 - 25) <= duckrect.bottom or (duckrect.left <= standrect.right and duckrect.bottom >= standrect.top) or (duckrect.right >= wellrect.left and duckrect.bottom >= wellrect.top):
						duck[3] = duck[5]	#jump height
						duck[1] += duck[3] 
					
				if event.key == pygame.K_UP:
					if (480 - 25) <= gooserect.bottom or (gooserect.left <= standrect.right and gooserect.bottom >= standrect.top) or (gooserect.right >= wellrect.left and gooserect.bottom >= wellrect.top):
						goose[3] = goose[5]	#jump height
						goose[1] += goose[3]	

		if pygame.key.get_pressed()[pygame.K_a]:
			if (0 <= duckrect.left and standrect.top+4 >= duckrect.bottom) or standrect.right < duckrect.left:	#if the duck is to the right of the left side of the wall
				duck[0] -= duck[2]

		if pygame.key.get_pressed()[pygame.K_d]:
			if (width >= duckrect.right and wellrect.top+4 >= duckrect.bottom) or wellrect.left > duckrect.right:
				duck[0] += duck[2]

		if pygame.key.get_pressed()[pygame.K_LEFT]:
			if (0 <= gooserect.left and standrect.top+4 >= gooserect.bottom) or standrect.right < gooserect.left:	#if the duck is to the right of the left side of the wall
				goose[0] -= goose[2]

		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			if (width >= gooserect.right and wellrect.top+4 >= gooserect.bottom) or wellrect.left > gooserect.right:
				goose[0] += goose[2]

		#background
		screen.fill(backgroundcolour)
		screen.fill((25, 225, 25), grass) #pygame.draw.rect(screen, (25, 225, 25), (0, height-25, width, 25))

		#duck
		duckrect.x = duck[0]
		duckrect.y = duck[1] 
		screen.blit(duckpicture, duckrect)
		#duck y direction
		if ((height - 25) >= duckrect.bottom and (duckrect.left > standrect.right-4 and duckrect.right < wellrect.left+4)) or (duckrect.bottom <= standrect.top):
			duck[1] += duck[3]
			duck[3] += duck[4]

		#goose
		gooserect.x = goose[0]
		gooserect.y = goose[1]
		screen.blit(goosepicture, gooserect)
		#goose y direction
		if ((height - 25) >= gooserect.bottom and (gooserect.left > standrect.right-4 and gooserect.right < wellrect.left+4)) or (gooserect.bottom <= standrect.top):
			goose[1] += goose[3]
			goose[3] += goose[4]		

		#egg
		if int(seconds*100)/100 % 1 == 0:	#rate of eggs
			createegg(eggs)	

		drawegg(eggs)

		#obstacles
		standrect.x = 0
		standrect.y = height - 100 - 25
		screen.blit(standpicture, standrect)

		wellrect.x = width - 80
		wellrect.y = height - 100 - 25
		screen.blit(wellpicture, wellrect)

		#boost pad
		boostrect.x = width//2 - 50
		boostrect.y = height - 25 - 30
		screen.blit(boostpicture,boostrect)
		boostpad(boostrect, duckrect, gooserect)

		#scoring
		eggcatch(eggs, duckrect, gooserect)

		displayduckscore = font.render("duck score: " + str(duckhit), True, (0,0,0))
		screen.blit(displayduckscore, (30-15, 15))

		displaygoosescore = font.render("goose score: " + str(goosehit), True, (0,0,0))
		screen.blit(displaygoosescore, (height-5, 15))

		#time
		seconds -= 1/60

		timething = "time: " + str (seconds//0.1 / 10)

		displayseconds = font.render(timething, True, (0,0,0))
		screen.blit(displayseconds, (width/2-45, 15))

	elif seconds < 0: #end screen

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		# if seconds != -1:
		# 	pygame.mixer.music.stop()
		# 	pygame.mixer.music.unload()

		seconds = -1

		grass = pygame.Rect(0, height-100, width, 100)
		screen.fill((110, 255, 255))
		screen.fill((25, 225, 25), grass)

		font = pygame.font.SysFont("comicsansms", 30)
		displayduckscore = font.render("duck score: " + str(duckhit), True, (0,0,0))
		screen.blit(displayduckscore, (30, 230))

		displaygoosescore = font.render("goose score: " + str(goosehit), True, (0,0,0))
		screen.blit(displaygoosescore, (height-25, 230))


		if goosehit > duckhit:
			font = pygame.font.SysFont("monospaced", 70) 
			screen.blit(font.render("The winner is the goose!", True, (0,0,0)), (40, 15))

			duckpicture = pygame.transform.scale(pygame.image.load("duck.jpg"), (41*2, 54*2))
			duckrect = duckpicture.get_rect()
			rotateduckpicture = pygame.transform.rotate(duckpicture, 270)
			rotateduckrect = rotateduckpicture.get_rect()
			rotateduckrect.x = width/2 - 54
			rotateduckrect.y = 300
			screen.blit(rotateduckpicture,rotateduckrect)

			goosepicture = pygame.transform.scale(pygame.image.load("goose.jpg"), (41*2,54*2))
			gooserect = goosepicture.get_rect()
			gooserect.x = width/2 - 41
			gooserect.y = 200
			screen.blit(goosepicture,gooserect)
		
		elif goosehit < duckhit:
			font = pygame.font.SysFont("monospaced", 70) 
			screen.blit(font.render("The winner is the duck!", True, (0,0,0)), (40, 15))

			goosepicture = pygame.transform.scale(pygame.image.load("goose.jpg"), (41*2, 54*2))
			gooserect = goosepicture.get_rect()
			rotategoosepicture = pygame.transform.rotate(goosepicture, 270)
			rotategooserect = rotategoosepicture.get_rect()
			rotategooserect.x = width/2 - 54
			rotategooserect.y = 300
			screen.blit(rotategoosepicture,rotategooserect)

			duckpicture = pygame.transform.scale(pygame.image.load("duck.jpg"), (41*2,54*2))
			duckrect = duckpicture.get_rect()
			duckrect.x = width/2 - 41
			duckrect.y = 200
			screen.blit(duckpicture,duckrect)
		
		else:
			font = pygame.font.SysFont("monospaced", 70) 
			screen.blit(font.render("It's a tie!", True, (0,0,0)), (230, 15))

			duckpicture = pygame.transform.scale(pygame.image.load("duck.jpg"), (41*2,54*2))
			duckrect = duckpicture.get_rect()
			duckrect.x = width/2 - 41 - 50
			duckrect.y = 272
			screen.blit(duckpicture,duckrect)

			goosepicture = pygame.transform.scale(pygame.image.load("goose.jpg"), (41*2,54*2))
			gooserect = goosepicture.get_rect()
			gooserect.x = width/2 - 41 + 50
			gooserect.y = 272
			screen.blit(goosepicture,gooserect)

	pygame.display.flip()
	time.sleep(1/60)