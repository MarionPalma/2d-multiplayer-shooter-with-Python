import pygame
from pygame import mixer
from player import Player
from bullet import Bullet

#zorgt ervoor dat er geen vertraging klinkt bij bullet afvuren
pygame.mixer.pre_init(44100, -16, 1, 512)

# pygame initialiseren
pygame.init()

# screen aanmaken
screen = pygame.display.set_mode((700, 500))

#titel game
pygame.display.set_caption("2D Multiplayer Shooter")

# achtergrond laden
background = pygame.image.load('image/war-background.jpg')

# players laden
player1Image = pygame.image.load('image/player1.png')
player2Image = pygame.image.load('image/player2.png')

#bullets laden
bulletPlayer1Image = pygame.image.load('image/kogel-player1.png')
bulletPlayer2Image = pygame.image.load('image/kogel-player2.png')

#score variabelen
scorePlayer1 = 0
scorePlayer2 = 0
fontScore = pygame.font.Font('freesansbold.ttf', 40)

#score winner variabele
fontWinner = pygame.font.Font('freesansbold.ttf', 64)

#functie scores op scherm krijgen
def display_score_players(x,y):
    score = fontScore.render(str(scorePlayer2) + " - " + str(scorePlayer1), True, (0, 0, 0) )
    screen.blit(score, (x, y))

#functie winner
def display_winner(x, y, winnerplayer):
    winner = fontScore.render(winnerplayer + " heeft gewonnen!", True, (0, 0, 0))
    screen.blit(winner, (x,y))


#achtergrond en shot sound laden
mixer.music.load('sounds/background-music.mp3')
mixer.music.play(-1)
shotSound = mixer.Sound('sounds/shot-sound.ogg')

#aanmaken players (objecten)
p1 = Player(626, 400)
p2 = Player(10, 10)

#aanmaken bullets (objecten)
b1 = Bullet(p1.x)
b2 = Bullet(p2.x +15)

# game loop
running = True
while running:
    # blit() method aanroepen om achtergrond afbeelding op scherm te krijgen
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #de status van alle toetsenbord knoppen ophalen
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        p1.y -= 2
    if keys[pygame.K_DOWN]:
        p1.y += 2
    if keys[pygame.K_w]:
        p2.y -=2
    if keys[pygame.K_s]:
        p2.y +=2
    if keys[pygame.K_SPACE]:
        if b1.state == "ready":
            shotSound.play()
            b1.y = p1.y
            b1.state = "fire"
    if keys[pygame.K_d]:
        if b2.state == "ready":
            shotSound.play()
            b2.y = p2.y
            b2.state = "fire"

    # Als state van bullet "fire" is, dan bullet op scherm laten vertonen en schieten
    if b1.state == "fire":
        b1.draw(screen, bulletPlayer1Image, b1.y)
        b1.x -= 3
    if b2.state == "fire":
        b2.draw(screen, bulletPlayer2Image, b2.y)
        b2.x += 3
    # Bullets resetten als zijkant van scherm wordt geraakt, zodat player daarna opnieuw kan schieten
    if b1.x <= 0:
        b1.x = p1.x
        b1.state = "ready"
    if b2.x >= 676:
        b2.x = p2.x
        b2.state = "ready"



    #grenzen oproepen
    p1.boundaries(p1.y)
    p2.boundaries(p2.y)

    #objecten op scherm plaatsen
    p1.draw(screen, player1Image)
    p2.draw(screen, player2Image)

    #coordinaten rechthoeken
    player1Rect = pygame.Rect(p1.x, p1.y, 64, 64)
    player2Rect = pygame.Rect(p2.x, p2.y, 64, 64)
    bullet1Rect = pygame.Rect(b1.x, b1.y, 24, 24)
    bullet2Rect = pygame.Rect(b2.x, b2.y, 24, 24)

    if bullet1Rect.colliderect(player2Rect):
        scorePlayer1 += 1
        b1.x = p1.x
        b1.state = "ready"
    if bullet2Rect.colliderect(player1Rect):
        scorePlayer2 += 1
        b2.x = p2.x
        b2.state = "ready"

    #scores op scherm tonen
    display_score_players(300, 450)

    #winner bepalen
    if scorePlayer1 == 3:
        b1.state = "stop"
        b2.state = "stop"
        display_winner(120, 200, "Player 1")
    if scorePlayer2 == 3:
        b1.state = "stop"
        b2.state = "stop"
        display_winner(120, 200, "Player 2")

    #update het scherm
    pygame.display.update()


#troubelshooting:
# geen naam van game op scherm. blit methode niet goed?
