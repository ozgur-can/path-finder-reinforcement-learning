# coding=utf-8
import pygame
import random

# pygame settings

pygame.init()

green = (77, 213, 153)
blue = (0, 51, 102)
red = (225, 51, 51)
white = (225, 255, 255)

width = 500
height = 500

boxSize = 50

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Finding Terminal')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


class Box():  # hedefe gidecek olan nesne

    x = 0
    y = 0
    w = 20

    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def MoveTo(self, x, y):
        self.x = x
        self.y = y

    def Show(self):
        pygame.draw.rect(screen, blue, [self.x, self.y, self.w, self.w])


class Trap():  # hedefe giderken yoldaki engellerin her biri

    x = 0
    y = 0
    w = 20

    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def Show(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.w, self.w])


class Terminal():  # hedef nesnesi

    x = 0
    y = 0
    w = 20

    def __init__(self, w):
        self.x = width - w
        self.y = height - w
        self.w = w

    def Show(self):
        pygame.draw.rect(screen, red, [self.x, self.y, self.w, self.w])


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
        self.rTable[3][1] = -1
        self.rTable[3][2] = -1
        self.rTable[3][3] = -1
        self.rTable[3][4] = -1

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
        box = Box(0, 0, boxSize)
        terminal = Terminal(boxSize)
        traps = []

        # tuzaklarin listeye eklenmesi
        for idx, i in enumerate(sim.rTable):
            for idj, j in enumerate(i):
                if j == -1:
                    traps.append(Trap(idx * boxSize, idj * boxSize, boxSize))

        while not self.isStarted:
            screen.fill(green)
            box.Show()
            terminal.Show()
            for trap in traps:
                trap.Show()

            # hedefe ulasma durumu
            if box.x == terminal.x & box.y == terminal.y:
                self.genNumber += 1
                box.MoveTo(0, 0)
                # q tablosu guncellenecek burada(!)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isStarted = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isStarted = True
                    if event.key == pygame.K_LEFT:
                        box.MoveTo(box.x - boxSize, box.y)
                    if event.key == pygame.K_RIGHT:
                        box.MoveTo(box.x + boxSize, box.y)
                    if event.key == pygame.K_UP:
                        box.MoveTo(box.x, box.y - boxSize)
                    if event.key == pygame.K_DOWN:
                        box.MoveTo(box.x, box.y + boxSize)

            clock.tick(7)


sim = Program()
sim.SetInitsForTables()
sim.Loop()

# TODOS
# (2) algoritma kısmına başla
# (3) q tablosunu guncelle
# print(random.randrange(0, 100)) random sayi tutmak icin kullan
