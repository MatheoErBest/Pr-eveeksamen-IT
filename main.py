import pygame
import pymysql
import sys
import random

# Farger
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
Usikker = (128, 40, 0)

# Funksjon som legger til en popup for å logge inn
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
    user_id = ''
    user_pass = ''
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
                    if user_id != '' and user_pass != '':
                        if login_user(user_id, user_pass):
                            done = True
                        else:
                            error_message = "User not found. Please register."
                elif register_button.collidepoint(event.pos):
                    register_user(user_id, user_pass)
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
                        user_id = user_id[:-1]
                    else:
                        user_id += event.unicode
                elif active_password:
                    if event.key == pygame.K_RETURN:
                        if user_id != '' and user_pass != '':
                            if login_user(user_id, user_pass):
                                done = True
                            else:
                                error_message = "User not found. Please register."
                    elif event.key == pygame.K_BACKSPACE:
                        user_pass = user_pass[:-1]
                    else:
                        user_pass += event.unicode

        screen.fill((30, 30, 30))

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Enter your username:", True, (255, 255, 255))
        screen.blit(text_surface, (100, 100))

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Enter your password:", True, (255, 255, 255))
        screen.blit(text_surface, (400, 100))

        # Login knapp
        pygame.draw.rect(screen, (0, 100, 0), login_button if login_selected else color_inactive_button)
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Login", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=login_button.center)
        screen.blit(text_surface, text_rect)

        # Registreringsknapp
        pygame.draw.rect(screen, (0, 100, 0), register_button if not login_selected else color_inactive_button)
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Register", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=register_button.center)
        screen.blit(text_surface, text_rect)

        txt_surface_username = pygame.font.Font(None, 32).render(user_id, True, color)
        width_username = max(200, txt_surface_username.get_width()+10)
        input_box_username.w = width_username
        screen.blit(txt_surface_username, (input_box_username.x+5, input_box_username.y+5))
        pygame.draw.rect(screen, color, input_box_username, 2)

        txt_surface_password = pygame.font.Font(None, 32).render("*" * len(user_pass), True, color)
        width_password = max(200, txt_surface_password.get_width()+10)
        input_box_password.w = width_password
        screen.blit(txt_surface_password, (input_box_password.x+5, input_box_password.y+5))
        pygame.draw.rect(screen, color, input_box_password, 2)

        # Feilmelding
        if error_message:
            font = pygame.font.Font(None, 24)
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (100, 300))

        pygame.display.flip()

    return user_id, user_pass, login_selected

def register_user(user_id, password):
    connect = pymysql.connect(
        host='172.20.128.69',
        user='matheo',
        password='123Akademiet',
        database='bruker'
    )

    try:
        with connect.cursor() as cursor:
            # Sjekk om brukernavnet allerede eksisterer
            check_sql = "SELECT * FROM loggin WHERE id=%s"
            cursor.execute(check_sql, (user_id,))
            existing_user = cursor.fetchone()
            
            error_message = ''
            if existing_user:
                error_message = 'bruker eksisterer allerede'
                if error_message:
                    font = pygame.font.Font(None, 24)
                    error_surface = font.render(error_message, True, (255, 0, 0))
                    screen.blit(error_surface, (100, 300))
            
            # Legg til brukeren hvis den ikke allerede eksisterer
            insert_sql = "INSERT INTO loggin (id, password) VALUES (%s, %s)"
            cursor.execute(insert_sql, (user_id, password))
            connect.commit()
            return True  # Returner True for å indikere vellykket registrering
    finally:
        connect.close()


def login_user(username, password):
    connect = pymysql.connect(
        host='172.20.128.69',
        user='matheo',
        password='123Akademiet',
        database='bruker'
    )
    try:
        with connect.cursor() as cursor:
            sql = "SELECT * FROM loggin WHERE id=%s AND password=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    finally:
        connect.close()

# Funksjon for å sette inn score og brukernavn i database
def insert_score(username, score):
    connect = pymysql.connect(
        host='172.20.128.69',
        user='matheo',
        password='123Akademiet',
        database='spillinfo',
    )

    try:
        if username:
            # Update the score for the existing user
            cursor.execute("UPDATE score SET score = %s WHERE username = %s", (score, username))
        else:
            # Insert a new record for the user
            cursor.execute("INSERT INTO users (username, score) VALUES (%s, %s)", (username, score))

        with connect.cursor() as cursor:
            sql = "INSERT INTO score (id, score) VALUES (%s, %s)"
            cursor.execute(sql, (username, score))
            connect.commit()
    finally:
        connect.close()

# Display
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Enter Username')


# Funksjon for å starte spillet
def playGame():
    # Definerer vindusstørrelsen
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 700

    # Lager vinduet til programmet
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mitt spill")

    # Setter firkantens posisjon og størrelse
    square_x = 100
    square_y = 100
    square_width = 20
    square_height = 20

    # Bevegelseshastighet
    speed = 10

    # Liste over rom
    rooms = ["Rom1", "Rom2", "Rom3", "Rom4"]
    current_room_index = 0

    # Velger det første rommet
    current_room = rooms[current_room_index]

    # Score
    score = 0

    # Setter opp font for score
    font = pygame.font.Font(None, 36)

    # Størrelse på den skjulte gjenstanden
    hidden_item_width = 50
    hidden_item_height = 50

    # Setter opp hovedløkken til spillet
    running = True
    while running:
        # Hører etter hendelser
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Bytt til neste rom når mellomromstasten trykkes
                    current_room_index = (current_room_index + 1) % len(rooms)
                    current_room = rooms[current_room_index]

        # Håndterer tastetrykk
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
            username = 1234
            insert_score(username, score)
            running = False

        # Sørger for at firkanten ikke går utenfor vinduet
        square_x = max(0, min(square_x, WINDOW_WIDTH - square_width))
        square_y = max(0, min(square_y, WINDOW_HEIGHT - square_height))

        # Tegner bakgrunnen


        

        # Viser scoren øverst i midten av skjermen
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        win.blit(text, text_rect)

        

        # Sjekker om firkanten er i det riktige rommet
        if current_room == "Rom1":
            win.fill(WHITE)
        
        elif current_room == 'Rom2':
            win.fill(BLUE)

        elif current_room == 'Rom3':
            screen.fill(Usikker)

        elif current_room == 'Rom4':
            screen.fill(WHITE)
            pygame.draw.rect(win, BLUE, (100, 100, hidden_item_width, hidden_item_height))
            if 75 <= square_x <= 125:
                if 75 <= square_y <= 125:
                    score += 1

        # Tegner firkanten
        pygame.draw.rect(win, RED, (square_x, square_y, square_width, square_height))

        # Oppdaterer vinduet
        pygame.display.update()

# Display
pygame.init()
clock = pygame.time.Clock()
screenX, screenY = 1080, 700
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Super Duper Kul')

# Vis popup-vinduet for å få brukernavnet
show_popup(screen)

# Funksjoner for hovedmenyen
def drawText(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def screenUpdate():
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

def changeRes():
    res = 'liten'

    if res == 'liten':
        screenX, screenY = 1080, 1620
        res = 'stor'
        pygame.display.update()
    
    if res == 'stor':
        screenX, screeny = 900, 1000
        res = 'liten'
        pygame.display.update()

highscore = 300

# Meny verdier
menuItems = ['Start game', 'Options', 'Exit']
selectedItem = 0
in_options_menu = False

# Alternativmeny verdier
optionMenuItems = ['Resolution', 'Sound', 'Controls', 'Back']
selectedOptionItem = 0

keys = pygame.key.get_pressed()
# Hovedløkke for hovedmenyen
Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if not in_options_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selectedItem = (selectedItem + 1) % len(menuItems)
                elif event.key == pygame.K_UP:
                    selectedItem = (selectedItem - 1) % len(menuItems)
                elif event.key == pygame.K_RETURN:
                    if selectedItem == 0:                        
                        playGame()  # Starter spillet når "Start game" er valgt
                    elif selectedItem == 1:
                        in_options_menu = True
                    elif selectedItem == 2:
                        pygame.quit()
                        sys.exit()

        elif in_options_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selectedOptionItem = (selectedOptionItem + 1) % len(optionMenuItems)
                elif event.key == pygame.K_UP:
                    selectedOptionItem = (selectedOptionItem - 1) % len(optionMenuItems)
                elif event.key == pygame.K_RETURN:
                    if selectedOptionItem == 0:
                        changeRes()
                    if selectedOptionItem == 3:  # Back option selected
                        in_options_menu = False
                elif event.key == pygame.K_BACKSPACE:
                    in_options_menu = False
               

    # Tegne menyen
    if not in_options_menu:
        screen.fill((0, 0, 0))
        menu_font = pygame.font.Font(None, 36)
        for i, item in enumerate(menuItems):
            color = (255, 255, 255) if i == selectedItem else (128, 128, 128)
            drawText(item, menu_font, color, screenX // 2, 200 + i * 50)
            drawText("Use UP / Down Arrow Keys To Navigate And Enter To Choose", menu_font, (128, 128, 128), screenX // 2, 400)

    if in_options_menu:
        screen.fill((0, 0, 0))
        sub_menu_font = pygame.font.Font(None, 36)
        for i, item in enumerate(optionMenuItems):
            color = (255, 255, 255) if i == selectedOptionItem else (128, 128, 128)
            drawText(item, sub_menu_font, color, screenX // 2, 200 + i * 50)
            drawText("Press Backspace to go back", sub_menu_font, (128, 128, 128), screenX // 2, 400)

    screenUpdate()

pygame.quit()
sys.exit()