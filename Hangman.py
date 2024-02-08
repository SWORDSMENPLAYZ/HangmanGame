# import
import pygame as pg
import sys, random, time

pg.init()

# constants
RES = WIDTH, HEIGHT = (800, 500)
FPS = 30

font = pg.font.SysFont("Arial", 36)
game_over = False
row = 2
columns = 13
gap = 20
size = 40

# creates boxes
boxes = []
for row in range(row):
    for col in range(columns):
        x = ((col * gap) + gap) + (col * size)
        y = ((row * gap) + gap) + (row * size) + 350
        box = pg.Rect(x, y, size, size)
        boxes.append(box)

#creates letters
letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
button_text = iter(letters)

screen = pg.display.set_mode(RES)

#renders the boxes
for box in boxes:
    text_surface = font.render(next(button_text), True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=box.center)
    screen.blit(text_surface, text_rect)

buttons = []
A = 65

#puts letters in boxes
for ind, box in enumerate(boxes):
    letter = chr(A + ind)
    button = [box, letter]
    buttons.append(button)

#draws buttons
def draw_buttons(buttons):
    for box, letter in buttons:
        btn_text = font.render(letter, True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect(center=(box.x + 20, box.y + 20))
        screen.blit(btn_text, btn_text_rect)

#letter guessing checker
def display_guess(guess):
    guess = str(guess).lower()
    display_text = ''
    for letter in word:
        if letter in guess:
            display_text += letter.upper() + ' '
        else:
            display_text += '_ '
    text = letter_font.render(display_text, True, (0, 0, 0))
    screen.blit(text, (400, 200))

# load images
images = [pg.image.load(f'Images/{index}.png') for index in range(6)]
image = images[0]  # default to the first image

hangman_status = 0

#words for the game
words = ['python', 'java', 'kotlin', 'Code']
word = random.choice(words)
guessed = []

#fonts
letter_font = pg.font.SysFont("Arial", 60)
font = pg.font.SysFont("Arial", 30)
game_font = pg.font.SysFont("Arial", 80)

#renders the location and contexts of the title
title = "Hangman"
title_text = game_font.render(title, True, (0, 0, 0))
title_rect = title_text.get_rect(center=(WIDTH // 2,
                                         title_text.get_height() // 2 + 10))

# intialize pygame
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()

#draws the hangman 
running = True
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            click_pos = event.pos
            for button, letter in buttons:
                if button.collidepoint(click_pos):
                    print(letter.lower(), word)
                    if letter.lower() not in word:
                        hangman_status += 1
                        if hangman_status == 6:
                            game_over = True
                        buttons.remove([button, letter])
                    if letter.lower() in word:
                        buttons.remove([button, letter])
                        guessed.append(letter)
            for i in range(5):
                image = pg.image.load("Images/" + str(hangman_status) + ".png")
                if hangman_status == 6:
                    running = False

    #checks for win/loss
    screen.blit(image, (150, 150))
    for box in boxes:
        pg.draw.rect(screen, (0, 0, 0), box, 2)
        won = True
        for letter in word:
            if letter not in str(guessed).lower():
                won = False
        if won:
            game_over = True
            game_text = "YOU WON!"

        elif game_over:
            game_text = "YOU LOST"

        #adds new screen once game over    
        draw_buttons(buttons) 
        display_guess(guessed)
        screen.blit(title_text, title_rect)
        if game_over:
            screen.fill((255, 255, 255))

            # render "Your word is:"
            endgame_text = font.render("Your word was: ", True, (0, 0, 0))
            endgame_text_x = 1  # change the X pos  
            endgame_text_y = 1  # change the Y pos
            screen.blit(endgame_text, (endgame_text_x, endgame_text_y))

            # render and blit the word
            word_text = font.render(word, True, (0, 0, 0))
            word_text_x = endgame_text_x + endgame_text.get_width() + 10  # Adjust the X pos
            word_text_y = endgame_text_y  # Keep the same Y position as "Your word is: "
            screen.blit(word_text, (word_text_x, word_text_y))

            # render and blit other text
            text = game_font.render(game_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            pg.display.update()
            pg.time.delay(3000)
            pg.quit()


    
    pg.display.update()
    pg.display.set_caption(str(clock.get_fps()))
