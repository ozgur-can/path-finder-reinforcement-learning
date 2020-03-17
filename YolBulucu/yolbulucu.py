import pygame
import random

# pygame settings

pygame.init()

green = (77, 213, 153)  # box color
black = (0, 0, 0)  # trap box color
blue = (50, 153, 213)  # terminal box color

width = 500
height = 500

dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Finding Terminal')

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

mesg = font_style.render("msg", True, green)
dis.blit(mesg, [width / 6, height / 3])

pygame.draw.rect(dis, blue, [40, 30, 10, 10])


class Box():  # hedefe gidecek olan nesne

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Trap():  # hedefe giderken yoldaki engellerin her biri

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Terminal():  # hedef nesnesi

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Program():
    alfa = 0.1
    discountFactor = 1
    rows = 5
    cols = 5
    reward = 100
    qTable = []
    rTable = []
    isStarted = False
    genNumber = 1

    def SetTraps(self):
        self.rTable[1][1] = -1
        self.rTable[2][1] = -1
        self.rTable[3][1] = -1

    # r ve q tablosuna ilk atamalar yapildi
    def SetInitsForTables(self):
        # r tablosu atandi
        for i in range(self.rows):
            self.rTable.append([])
            for j in range(self.cols):
                if i == self.rows - 1 & j == self.cols - 1:
                    self.rTable[i].append(self.reward)
                else:
                    self.rTable[i].append(0)
        self.SetTraps()

        # q tablosu atandi // baska duzenleme olmayacak
        for i in range(self.rows):
            self.qTable.append([])
            for j in range(self.cols):
                self.qTable[i].append(0)

    def Loop(self):
        while not self.isStarted:
            dis.fill(green)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isStarted = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isStarted = True


p = Program()
p.SetInitsForTables()
p.Loop()

# print(random.randrange(0, 100))
