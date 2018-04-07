import pygame,sys,random,time

check_erros=pygame.init()

playSurface=pygame.display.set_mode((720,460)) #Tamaño de pantalla
pygame.display.set_caption('Snake game!') #Nombre de la ventana
fpsController = pygame.time.Clock() #Controlador de fps (velocidad en el juego)

#Colores
red = pygame.Color(255, 0, 0) # game over
green = pygame.Color(0, 255, 0) # snake body
black = pygame.Color(0, 0, 0) # score
white = pygame.Color(255, 255, 255) # bg
brown = pygame.Color(165, 42, 42) # food

snakePos = [100, 50] #Posicion inicial de la serpiente coordenadas[X,Y]
snakeBody = [[100, 50], [90, 50], [80, 50]] #Cuerpo de la serpiente, lista de bloques
foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10] #Posicion random inicial de la comida
foodSpawm = True #Sirve para saber si hay comido en el tablero
direction = 'RIGHT' #Direccion actual
score = 0 

def gameOver():
    myFont = pygame.font.SysFont('comicsansms', 60)  # type and size #pygame module for loading and rendering fonts
    GOtext = myFont.render('Game Over', True, red)
    GOrect = GOtext.get_rect()  # get the rectangular area of the Surface
    GOrect.midtop = (360, 15)
    playSurface.blit(GOtext, GOrect)  # surface and rectangle #draw one image onto another
    showScore(0)
    pygame.display.flip()  # update function
    time.sleep(3)
    pygame.quit()  # pygame window exit
    sys.exit()  # console exit

def getEvent(dir):
    for event in pygame.event.get():  #Obtenemos los eventos del usuario
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                dir = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                dir = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                dir= 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                dir = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    return dir

def moveSnake(direction):
    #mueve a la serpiente modificando los valores de X & Y
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10
    snakeBody.insert(0, list(snakePos)) #snake mechanism #modifica a la serpiente
    return snakePos, snakeBody

def boundaries(snakePos, snakeBody):
    #Pone limite a la serpiente cuando golpea alguna de las paredes
    if snakePos[0] > 710 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()
    #Pone limite a la serpiente cuando se golpea a si misma
    for block in snakeBody[1:]: 
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

def showScore(choice=1):
    sFont = pygame.font.SysFont('comicsansms', 25)
    sText = sFont.render('Score: {0}'.format(score), True, black)
    sRect = sText.get_rect()
    if choice == 1: #choice default
      sRect.midtop = (80, 10)
    else: #cualquier otro parametro diferentente a 1
        sRect.midtop = (360, 120)
    playSurface.blit(sText, sRect)

if __name__ == "__main__":
    if check_erros[1]>0:
        print("(!) Had {0} initializing errors, exiting ...".format(
        check_errors[1]))
        sys.exit(-1)
    else:
        print("(+) PyGame successfully initialized!")
        
    while True:
        playSurface.fill(white)
        changeto=getEvent(direction)
        
        if changeto == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeto == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeto == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeto == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        
        snakePos,snakeBody=moveSnake(direction)
        
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            score += 6
            foodSpawm = False
        else:
            snakeBody.pop()
            if foodSpawm == False:
                foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
                foodSpawm = True
        for pos in snakeBody:
            pygame.draw.rect(playSurface, green,
            pygame.Rect(pos[0], pos[1], 10, 10))
        
        pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))
        boundaries(snakePos,snakeBody)
        showScore()
        
        pygame.display.flip()  # updating display
        fpsController.tick(25) 
