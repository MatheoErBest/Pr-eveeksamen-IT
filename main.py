import pygame
import pymysql
import sys
import random
from argon2 import PasswordHasher
ph = PasswordHasher()

# Colors
black = (127, 127, 127, 255)
blue = (127, 127, 255, 255)
cyan = (127, 255, 255, 255)
gold = (255, 235, 127, 255)
gray = (222, 222, 222, 255)
green = (127, 255, 127, 255)
orange = (255, 210, 127, 255)
purple = (207, 143, 247, 255)
red = (255, 127, 127, 255)
violet = (246, 192, 246, 255)
yellow = (255, 255, 127, 255)
white = (255, 255, 255, 255)

def hash_password(user_passord):
    return ph.hash(user_passord)

# Function to show login/register popup
def show_popup(screen):
    input_box_username = pygame.Rect(100, 150, 140, 32)
    input_box_password = pygame.Rect(400, 150, 140, 32)
    login_button = pygame.Rect(100, 250, 120, 50)
    register_button = pygame.Rect(400, 250, 120, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active_username = False
    active_password = False
    user_brukernavn = ''
    user_passord = ''
    hashed_passord = ''
    done = False
    login_selected = True
    color_inactive_button = pygame.Color('darkgreen')
    error_message = ''

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    active_username = True
                    active_password = False
                elif input_box_password.collidepoint(event.pos):
                    active_username = False
                    active_password = True
                elif login_button.collidepoint(event.pos):
                    if user_brukernavn != '' and user_passord != '':
                        if login_user(user_brukernavn, user_passord):
                            done = True
                        else:
                            error_message = "User not found. Please register."
                elif register_button.collidepoint(event.pos):
                    register_user(user_brukernavn, user_passord, screen)
                else:
                    active_username = False
                    active_password = False
                color = color_active if active_username or active_password else color_inactive

            if event.type == pygame.KEYDOWN:
                if active_username:
                    if event.key == pygame.K_RETURN:
                        active_username = False
                        active_password = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_brukernavn = user_brukernavn[:-1]
                    else:
                        user_brukernavn += event.unicode
                elif active_password:
                    if event.key == pygame.K_RETURN:
                        if user_brukernavn != '' and user_passord != '':
                            if login_user(user_brukernavn, user_passord):
                                done = True
                            else:
                                error_message = "User not found. Please register."
                    elif event.key == pygame.K_BACKSPACE:
                        user_passord = user_passord[:-1]
                    else:
                        user_passord += event.unicode

        screen.fill((30, 30, 30))

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Enter your username:", True, (255, 255, 255))
        screen.blit(text_surface, (100, 100))

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Enter your password:", True, (255, 255, 255))
        screen.blit(text_surface, (400, 100))

        # Login button
        pygame.draw.rect(screen, (0, 100, 0), login_button if login_selected else color_inactive_button)
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Login", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=login_button.center)
        screen.blit(text_surface, text_rect)

        # Register button
        pygame.draw.rect(screen, (0, 100, 0), register_button if not login_selected else color_inactive_button)
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Register", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=register_button.center)
        screen.blit(text_surface, text_rect)

        txt_surface_username = pygame.font.Font(None, 32).render(user_brukernavn, True, color)
        width_username = max(200, txt_surface_username.get_width()+10)
        input_box_username.w = width_username
        screen.blit(txt_surface_username, (input_box_username.x+5, input_box_username.y+5))
        pygame.draw.rect(screen, color, input_box_username, 2)

        txt_surface_password = pygame.font.Font(None, 32).render("*" * len(user_passord), True, color)
        width_password = max(200, txt_surface_password.get_width()+10)
        input_box_password.w = width_password
        screen.blit(txt_surface_password, (input_box_password.x+5, input_box_password.y+5))
        pygame.draw.rect(screen, color, input_box_password, 2)

        # Error message
        if error_message:
            font = pygame.font.Font(None, 24)
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (100, 300))

        pygame.display.flip()

    return user_brukernavn, user_passord, login_selected

def register_user(user_brukernavn, passord, screen):
    connect = pymysql.connect(
        host='172.20.128.56',
        user='matheo',
        password='123Akademiet',
        database='bruker'
    )

    try:
        with connect.cursor() as cursor:
            # Check if username already exists
            check_sql = "SELECT * FROM bruker WHERE brukernavn=%s"
            cursor.execute(check_sql, (user_brukernavn,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error_message = 'User already exists'
                if error_message:
                    font = pygame.font.Font(None, 24)
                    error_surface = font.render(error_message, True, (255, 0, 0))
                    screen.blit(error_surface, (100, 300))
                    pygame.display.flip()
                    return False
            
            # Add the user if it doesn't already exist
            insert_sql = "INSERT INTO bruker (brukernavn, passord) VALUES (%s, %s)"
            cursor.execute(insert_sql, (user_brukernavn, passord))
            connect.commit()
            return True  # Return True to indicate successful registration
    finally:
        connect.close()

def login_user(username, password):
    password = hash_password(password)
    connect = pymysql.connect(
        host='172.20.128.56',
        user='matheo',
        password='123Akademiet',
        database='bruker'
    )
    try:
        with connect.cursor() as cursor:
            sql = "SELECT * FROM bruker WHERE brukernavn=%s AND passord=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    finally:
        connect.close()

# Function to insert score into database
def insert_score(username, score):
    connect = pymysql.connect(
        host='172.20.128.56',
        user='matheo',
        password='123Akademiet',
        database='spillinfo',
    )

    try:
        with connect.cursor() as cursor:
            if username:
                # Update the score for the existing user
                cursor.execute("UPDATE spillinfo SET highscore = %s WHERE brukernavn = %s", (score, username))
            else:
                # Insert a new record for the user
                cursor.execute("INSERT INTO spillinfo (brukernavn, highscore) VALUES (%s, %s)", (username, score))

            connect.commit()
    finally:
        connect.close()

#Classes
class Room:
    def __init__(self, name, color, hidden_item = None):
        self.name = name
        self.color = color
        self.hidden_item = hidden_item

    def draw(self, win, square_x, square_y, hidden_item_size, score):
        win.fill(self.color)
        if self.hidden_item:
            pygame.draw.rect(win, self.hidden_item['color'], (self.hidden_item['x'], self.hidden_item['y'], hidden_item_size, hidden_item_size))
            if self.hidden_item['x'] <= square_x <= self.hidden_item['x'] + hidden_item_size and \
               self.hidden_item['y'] <= square_y <= self.hidden_item['y'] + hidden_item_size:
                score += 1
        return score
class Teleporter:
    def __init__(self, name, color):
        pass

class Player:
    pass

# Display
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Enter Username')

# Function to start the game
def play_game(username):
    # Define window size
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 700

    # Create the game window
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("My Game")

    # Square position and size
    square_x = 100
    square_y = 100
    square_width = 20
    square_height = 20

    # Movement speed
    speed = 10

    # List of rooms
    rooms = [
        Room('Room1', red),
        Room('Room2', orange, hidden_item={'x': 100, 'y': 100, 'color': blue}),
        Room('Room3', yellow),
        Room('Room4', green, hidden_item={'x': 100, 'y': 100, 'color': blue}),
        Room('Room5', blue),
    ]

    current_room_index = 0
    current_room = rooms[current_room_index]

    hidden_item_size = 50

    # Score
    score = 0

    # Set up font for score
    font = pygame.font.Font(None, 36)

    # Main game loop
    game = True
    while game:
        # Listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Switch to next room when space is pressed
                    current_room_index = (current_room_index + 1) % len(rooms)
                    current_room = rooms[current_room_index]

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            square_y -= speed
        if keys[pygame.K_s]:
            square_y += speed
        if keys[pygame.K_a]:
            square_x -= speed
        if keys[pygame.K_d]:
            square_x += speed
        if keys[pygame.K_ESCAPE]:
            game = False
            

        # Prevent the square from going out of the window
        square_x = max(0, min(square_x, WINDOW_WIDTH - square_width))
        square_y = max(0, min(square_y, WINDOW_HEIGHT - square_height))

        # Draw the current room and update the score
        score = current_room.draw(win, square_x, square_y, hidden_item_size, score)

        # Draw the square
        pygame.draw.rect(win, black, (square_x, square_y, square_width, square_height))
    

        # Display the score at the top center of the screen
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        win.blit(text, text_rect)

        # Update the window
        pygame.display.update()

# Display
pygame.init()
clock = pygame.time.Clock()
screenX, screenY = 1080, 700
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Super Cool Game')

# Show popup to get username
username, password, login_selected = show_popup(screen)

# Functions for main menu
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def screen_update():
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

def change_res():
    global screenX, screenY
    res = 'small'

    if res == 'small':
        screenX, screenY = 1080, 1620
        res = 'large'
        pygame.display.update()
    
    if res == 'large':
        screenX, screenY = 900, 1000
        res = 'small'
        pygame.display.update()

highscore = 300

# Menu values
menu_items = ['Start game', 'Options', 'Exit']
selected_item = 0
in_options_menu = False

# Option menu values
option_menu_items = ['Resolution', 'Sound', 'Controls', 'Back']
selected_option_item = 0

# Main loop for main menu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not in_options_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:                        
                        play_game(username)  # Start the game when "Start game" is selected
                    elif selected_item == 1:
                        in_options_menu = True
                    elif selected_item == 2:
                        pygame.quit()
                        sys.exit()

        elif in_options_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option_item = (selected_option_item + 1) % len(option_menu_items)
                elif event.key == pygame.K_UP:
                    selected_option_item = (selected_option_item - 1) % len(option_menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_option_item == 0:
                        change_res()
                    if selected_option_item == 3:  # Back option selected
                        in_options_menu = False
                elif event.key == pygame.K_BACKSPACE:
                    in_options_menu = False

    # Draw the menu
    if not in_options_menu:
        screen.fill((0, 0, 0))
        menu_font = pygame.font.Font(None, 36)
        for i, item in enumerate(menu_items):
            color = (255, 255, 255) if i == selected_item else (128, 128, 128)
            draw_text(item, menu_font, color, screenX // 2, 200 + i * 50)
            draw_text("Use UP / Down Arrow Keys To Navigate And Enter To Choose", menu_font, (128, 128, 128), screenX // 2, 400)

    if in_options_menu:
        screen.fill((0, 0, 0))
        sub_menu_font = pygame.font.Font(None, 36)
        for i, item in enumerate(option_menu_items):
            color = (255, 255, 255) if i == selected_option_item else (128, 128, 128)
            draw_text(item, sub_menu_font, color, screenX // 2, 200 + i * 50)
            draw_text("Press Backspace to go back", sub_menu_font, (128, 128, 128), screenX // 2, 400)

    screen_update()

pygame.quit()
sys.exit()
