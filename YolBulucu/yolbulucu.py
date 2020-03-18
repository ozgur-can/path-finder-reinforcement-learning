# coding=utf-8
import pygame
import random

# pygame settings

pygame.init()

green = (77, 213, 153)
blue = (0, 51, 102)
red = (225, 51, 51)
white = (225, 255, 255)
black = (0, 0, 0)

width = 500
height = 500

boxSize = 50

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Finding Terminal')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def message(msg, color):
    msgToShow = font_style.render(msg, True, color)
    screen.blit(msgToShow, [width / 4, height / 2])


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
    alfa = 0.7
    discountFactor = 1
    rows = 10
    cols = 10
    reward = 100
    qTable = []
    rTable = []
    isStarted = False
    genCount = 1
    iteration = 10
    traps = []

    def SetTraps(self):
        # self.rTable[1][0] = -1
        # self.rTable[1][1] = -1
        self.rTable[1][2] = -1
        self.rTable[1][3] = -1
        self.rTable[1][4] = -1
        self.rTable[1][5] = -1
        self.rTable[1][6] = -1
        # self.rTable[3][3] = 20
        # self.rTable[3][1] = 30

    # r ve q tablosuna ilk atamalar yapildi
    def SetInitsForTables(self):
        # r table init
        for i in range(self.rows):
            self.rTable.append([])
            for j in range(self.cols):
                if i == self.rows - 1 & j == self.cols - 1:
                    self.rTable[i].append(self.reward)
                else:
                    self.rTable[i].append(0)
        self.SetTraps()

        # q table init
        for i in range(self.rows):
            self.qTable.append([])
            for j in range(self.cols):
                self.qTable[i].append(0)
                # self.qTable[i].append(round(random.uniform(0, 1.0), 1))

    def CalculateRValues(self, routes):
        values = []
        for route in routes:
            values.append(self.rTable[route[0]][route[1]])

        return values

    def CalculateQValues(self, routes):
        values = []
        for route in routes:
            values.append(self.qTable[route[0]][route[1]])

        return values

    # find available routes
    def FindRoutes(self, x, y):
        routes = []
        routesWithOutNegativeVal = []

        routes.append([x - 1, y])
        routes.append([x, y - 1])
        routes.append([x + 1, y])
        routes.append([x, y + 1])

        for route in routes:
            if route[0] > 0 or route[1] > 0 or route[0] > 0 and route[1] > 0:
                routesWithOutNegativeVal.append(route)

        for route in routesWithOutNegativeVal:
            for trap in self.traps:
                if route[0] == trap.x / boxSize and route[1] == trap.y / boxSize:
                    routesWithOutNegativeVal.remove(route)

        return routesWithOutNegativeVal

    def IsEnd(self):
        if self.genCount == self.iteration:
            return True
        else:
            return False

    def Loop(self):
        box = Box(200, 150, boxSize)
        terminal = Terminal(boxSize)

        # tuzaklarin listeye eklenmesi
        for idx, i in enumerate(sim.rTable):
            for idj, j in enumerate(i):
                if j == -1:
                    self.traps.append(Trap(idx * boxSize, idj * boxSize, boxSize))

        while not self.isStarted:
            if self.genCount == 10:
                message('reached to max genCount', black)
                pygame.display.update()

            else:
                screen.fill(green)
                box.Show()
                terminal.Show()
                for trap in self.traps:
                    trap.Show()

                routes = self.FindRoutes(box.x / boxSize, box.y / boxSize)
                qValues = self.CalculateQValues(routes)
                maxQValueIndex = qValues.index(max(qValues))

                routesForNext = self.FindRoutes(routes[maxQValueIndex][0], routes[maxQValueIndex][1])
                qValuesForNext = self.CalculateQValues(routesForNext)
                maxNextQValueIndex = qValuesForNext.index(max(qValuesForNext))

                qX = box.x / boxSize
                qY = box.y / boxSize
                self.qTable[qX][qY] = self.qTable[qX][qY] + self.alfa * (
                        self.rTable[routes[maxQValueIndex][0]][routes[maxQValueIndex][1]] + self.discountFactor *
                        self.qTable[routes[maxNextQValueIndex][0]][routes[maxNextQValueIndex][1]])

                box.MoveTo(routes[maxQValueIndex][0] * boxSize, routes[maxQValueIndex][1] * boxSize)

                if box.x == terminal.x & box.y == terminal.y and not self.IsEnd():
                    self.genCount += 1
                    box.MoveTo(0, 0)

                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isStarted = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isStarted = True

            clock.tick(7)


sim = Program()
sim.SetInitsForTables()
sim.Loop()

pygame.quit()
quit()

# print sim.qTable

# TODOS
# (2) algoritma kısmına başla(!!!)
# (3) q tablosunu guncelle
# print(random.randrange(0, 100)) random sayi tutmak icin kullan
