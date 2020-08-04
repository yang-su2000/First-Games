from random import randint
import math
import pygame
pygame.init()

# customize game (int)
gameSize = 400 # >= 20*split
split = 20 # >= 10
difficulty = 20 # 0~20


fontSize = round(gameSize/10)
font = pygame.font.SysFont('comicsansms', fontSize, True)
fontx = round(gameSize + gameSize/5)
fonty = round(gameSize/20)
bsize = round(gameSize/split)
bwide = round(gameSize/(split*20))
bside = round(gameSize/split - gameSize/(split*20))
gamebox = [[7] * split for i in range(split * 2)]

win = pygame.display.set_mode((gameSize * 2, gameSize * 2))
pygame.display.set_caption("Tetris")

colorBox = ['blue', 'grey', 'orange', 'yellow', 'green', 'purple', 'red', 'black']

clock = pygame.time.Clock()
score = 0

class box(object):
    def __init__(self, x, y, btype):
        self.x = x
        self.y = y
        self.btype = btype

    def validmove(self, x, y):
        if self.x + x >= 0 and self.x + x < split and self.y + y >= 0 and self.y + y < split * 2:
            return gamebox[self.y + y][self.x + x] == 7
        return False

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        drawbox(self.x, self.y, self.btype)

    def dedraw(self):
        drawbox(self.x, self.y, 7)
  
    def hit(self):
        if self.y >= 2 * split - 1:
            return True
        return gamebox[self.y + 1][self.x] < 7

    def validrotate(self, x, y):
        return self.validmove(y - self.y + x - self.x, y - self.y - x + self.x)

    def rotate(self, x, y):
        mx = x - self.x
        my = y - self.y
        print("x += " + str(y - self.y + x - self.x))
        print("y += " + str(y - self.y - x + self.x))
        self.x += my + mx
        self.y += my - mx

      
class piece(object):
    def __init__(self, btype):
        self.btype = btype
        self.x = round(split/2)
        self.y = 1
        self.boxes = []
        self.angle = 0
                              # torque: +
        if (self.btype == 0): # --+-
            self.y -= 1
            for i in range (-2, 2):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        elif (self.btype == 1): # -
                                # +--
            newBox = box(self.x, self.y - 1, self.btype)
            self.boxes.append(newBox)
            for i in range (0, 3):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        elif (self.btype == 2): #   -
                                # --+
            newBox = box(self.x, self.y - 1, self.btype)
            self.boxes.append(newBox)
            for i in range (-2, 1):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        elif (self.btype == 3): # --
                                # -+
            for j in range (-1, 1):
                for i in range (-1, 1):
                    newBox = box(self.x + i, self.y + j, self.btype)
                    self.boxes.append(newBox)
        elif (self.btype == 4): #  --
                                # --+
            for i in range (-1, 1):
                newBox = box(self.x + i, self.y - 1, self.btype)
                self.boxes.append(newBox)
            for i in range (-2, 0):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        elif (self.btype == 5): #  -
                                # -+-
            newBox = box(self.x, self.y - 1, self.btype)
            self.boxes.append(newBox)
            for i in range (-1, 2):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        elif (self.btype == 6): # --
                                #  -+
            for i in range (-2, 0):
                newBox = box(self.x + i, self.y - 1, self.btype)
                self.boxes.append(newBox)
            for i in range (-1, 1):
                newBox = box(self.x + i, self.y, self.btype)
                self.boxes.append(newBox)
        else:
            print ("not valid btype")

    def hit(self):
        self.dedraw()
        for box in self.boxes:
            if not box.validmove(0, 1):
                self.draw()
                return True
        return False

    def draw(self):
        for box in self.boxes:
            box.draw()

    def dedraw(self):
        for box in self.boxes:
            box.dedraw()

    def movedown(self):
        self.y += 1
        for box in self.boxes:
            box.move(0, 1)

    def moveleft(self):
        self.dedraw()
        for box in self.boxes:
            if not box.validmove(-1, 0):
                self.draw()
                return
        self.x -= 1
        for box in self.boxes:
            box.move(-1, 0)

    def moveright(self):
        self.dedraw()
        for box in self.boxes:
            if not box.validmove(1, 0):
                self.draw()
                return
        self.x += 1
        for box in self.boxes:
            box.move(1, 0)

    def combine(self): # optimization required
        res = False
        for j in range(0, split * 2):
            isfull = True
            for x in gamebox[j]:
                if x == 7:
                    isfull = False
            if isfull:
                res = True
                endy = j
                while endy > 0:
                    for x in range(0, split):
                        drawbox(x, endy, gamebox[endy - 1][x])
                    endy -= 1
        return res

    def rotate(self):
        if self.btype == 3: 
            return
        self.dedraw()
        for box in self.boxes:
            if not box.validrotate(self.x, self.y):
                self.draw()
                return
        for box in self.boxes:
            box.rotate(self.x, self.y)
        self.angle += 1
        

def printScreen(): # debug
    for lst in gamebox:
        for i in lst:
            print(int(i), end=' ')
        print(end='\n')
    print(end='\n')

def drawbox(x, y, btype):
    gamebox[y][x] = btype
    pygame.draw.rect(win, pygame.Color(colorBox[btype]), (x * bsize + bwide, y * bsize + bwide, bside, bside))

def redrawGameWindow():
    myPiece.draw()
    pygame.draw.rect(win, pygame.Color('black'), (gameSize + 1, 0, gameSize, gameSize * 2))
    text = font.render('Score: ' + str(score), 1, pygame.Color('white'))
    win.blit(text, (fontx, fonty))
    text = font.render('Max: ' + str(2**round(300/difficulty)), 1, pygame.Color('blue'))
    win.blit(text, (fontx, fonty * 5))
    #printScreen()
    pygame.display.update()

def setup():
    pygame.draw.rect(win, pygame.Color('black'), (0, 0, gameSize, gameSize * 2))
    text = font.render('Score: ' + str(score), 1, pygame.Color('white'))
    win.blit(text, (fontx, fonty))
    text = font.render('MaxScore: ' + str(300 * (20 - difficulty)), 1, pygame.Color('blue'))
    win.blit(text, (fontx, fonty * 5))
    for x in range(0, split + 1):
        pygame.draw.rect(win, pygame.Color('white'), (x * bsize, 0, bwide, gameSize*2))
    for y in range(0, split * 2 + 1):
        pygame.draw.rect(win, pygame.Color('white'), (0, y * bsize, gameSize, bwide))

#mainloop
newPiece = True
run = True

setup()
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                myPiece.moveleft()
            elif event.key == pygame.K_RIGHT:
                myPiece.moveright()
            elif event.key == pygame.K_SPACE:
                myPiece.rotate()

    if newPiece == True:
        print ("New Piece")
        myPiece = piece(randint(0, 6))
        
        newPiece = False
        if myPiece.hit() == True:
            print ("Game Over")
            pygame.time.delay(2000)
            break

    if myPiece.hit() == True:
        newPiece = True
        if myPiece.combine():
            score += 100
        continue
    else:   
        myPiece.movedown()
        pygame.time.delay(300 - difficulty*round(math.log(score+1,2)))

    score += 1
    redrawGameWindow()

pygame.quit()
