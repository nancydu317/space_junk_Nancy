# added junk collected counter to change levels
# add level transition screens

import pgzrun
import random

# define screen
WIDTH = 1000
HEIGHT = 600
SCOREBOX_HEIGHT = 60  # change to height of scoreboard

# count score
score = 0  # start off with zero points
junk_collect = 0
level = 0
level_transition = 0
lvl2_LIMIT = 5
lvl3_LIMIT = 10

# sprite speeds
junk_speed = 5
sat_speed = 3
debris_speed = 5
laser_speed = -5  # moving LEFT, so negative x direction

BACKGROUND_IMG = "game_background0"  # change to your file name
PLAYER_IMG = "player_ship"  # change to your file name
JUNK_IMG = "space_junk"  # change to your file name
SATELLITE_IMG = "satellite_adv"  # change to your file name
DEBRIS_IMG = "tesla_roadster"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"


def init():
    # INITIALIZE SPRITES
    global player, junks, satellite, debris, lasers
    # sprite_name = Actor("file_name", rect_pos = (x, y))
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 10, HEIGHT / 2)  # rect_position = (x, y)

    # initialize junk sprites
    junks = []  # list to keep track of junks
    for i in range(5):
        junk = Actor(JUNK_IMG)  # create a junk sprite
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.pos = (x_pos, y_pos)  # rect_position = (x, y)
        junks.append(junk)

    # initialize satellite
    satellite = Actor(SATELLITE_IMG)  # create sprite
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)  # rect_position

    # initialize debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500, -50)
    y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    # initialize lasers
    lasers = []  # empty list
    player.laserActive = 1  # add laserActive status to the player


# initialize start screen
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

def on_mouse_down(pos):
    global level, level_transition
    if start_button.collidepoint(pos):
        level = 1
        level_transition = 1
        print("START!")
    if instructions_button.collidepoint(pos):
        level = -1
        print("INSTRUCTIONS!")


# background music
# sounds.spacelife.play(-1)

# MAIN GAME LOOP___________________________________________
init()


def update():  # main update function
    global score, junk_collect, level, level_transition, BACKGROUND_IMG
    if level == -1:  # instructions screen
        BACKGROUND_IMG = "game_background1"
    if score >= 0 and level >= 1:  # level 1 transition screen
        if level_transition == 1:
            BACKGROUND_IMG = "game_background1"
            if keyboard.RETURN == 1:  # level 1 game screen
                level_transition = 2
        if level_transition == 2:
            BACKGROUND_IMG = "game_background1"
            updatePlayer()  # calling our player update function
            updateJunk()  # calling junk update function
        if junk_collect >= lvl2_LIMIT and level_transition <= 3:
            level = 2
            level_transition = 3
            BACKGROUND_IMG = "game_background2"
            if keyboard.RETURN == 1:
                level_transition = 4
        elif level_transition == 4:
            BACKGROUND_IMG = "game_background2"
            updatePlayer()
            updateJunk()
            updateSatellite()
        if junk_collect >= lvl3_LIMIT and level_transition <= 5:
            level = 3
            level_transition = 5
            BACKGROUND_IMG = "game_background3"
            if keyboard.RETURN == 1:
                level_transition = 6
        elif level_transition == 6:
            BACKGROUND_IMG = "game_background3"
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()

    if score < 0:  # game over
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = "game_background0"
            score = 0
            junk_collect = 0
            level = 0
            init()



def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0, 0))
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\nLEVEL 1\ncollect junk to increase your score\n\nLEVEL 2\ncollect junk and avoid active satellites\n\nLEVEL 3\ncollect junk, avoid active satellites, and shoot dead satellites\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 70), fontsize=35, color="white")
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level >= 1:
        player.draw()  # draw player sprite on screen
        for junk in junks:
            junk.draw()  # draw junk sprite on screen
    if level >= 2:
        satellite.draw()
    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()

    # game over screen
    if score < 0:
        game_over = "GAME OVER\npress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH / 2, HEIGHT / 2), fontsize=70, color="white")
        sounds.spacelife.stop()

    # show text on screen
    show_score = "Score: " + str(score)  # remember to convert score to a string
    screen.draw.text(show_score, topleft=(825, 15), fontsize=35, color="white")
    show_collect_value = "Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(650, 15), fontsize=35, color="white")
    show_level = "LEVEL "
    screen.draw.text(show_level, topleft=(450, 15), fontsize=35, color="white")

    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topleft=(450, 15), fontsize=35, color="white")

    if level_transition == 1 or level_transition == 3 or level_transition == 5:
        show_level_title = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center=(WIDTH/2, HEIGHT/2), fontsize=70, color="white")


# UPDATE SPRITES________________
def updatePlayer():
    # check for keyboard inputs
    if keyboard.up == 1:
        player.y += -5  # moving up is negative y-direction
    elif keyboard.down == 1:
        player.y += 5  # moving down is positive y-direction
    # prevent player from moving off screen - add boundaries
    if player.top < SCOREBOX_HEIGHT:
        player.top = SCOREBOX_HEIGHT
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    # check for firing lasers
    if keyboard.space == 1 and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)


def updateJunk():
    global score, junk_collect
    for junk in junks:  # add for loop
        junk.x += junk_speed  # same as junk.x = junk.x + 3

        collision = player.colliderect(junk)  # declare collision variable

        if junk.left > WIDTH or collision == 1:  # make junk reappear if move off screen
            x_pos = random.randint(-500, -50)  # start off screen
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1:  # if collisions occurs
            sounds.collect_pep.play()  # sound effect
            score += 1  # this is the same score = score + 1
            junk_collect += 1

def updateSatellite():
    global score
    satellite.x += sat_speed  # or just put 3
    collision = player.colliderect(satellite)

    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -15


def updateDebris():
    global score
    debris.x += debris_speed  # or just put 3
    collision = player.colliderect(debris)

    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score += -15


def updateLasers():
    global score
    for laser in lasers:
        laser.x += laser_speed
        # remove laser if off screen
        if laser.right < 0:
            lasers.remove(laser)
        # detect collisions
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint(-500, -50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5
            sounds.explosion.play()
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = random.randint(-500, -50)
            y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 10
            sounds.explosion.play()


# activating lasers (template code)____________________________________________________________________________________________

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1


def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list


pgzrun.go()  # function that runs our game loop

