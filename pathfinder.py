# coding=utf-8
import pygame
import random

# pygame oyun motoru ayarları

pygame.init()

green = (77, 213, 153)
blue = (0, 51, 102)
red = (225, 51, 51)
white = (225, 255, 255)
black = (0, 0, 0)

width = 300
height = 300

boxSize = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Path Finder')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)


def message(msg, color):
    msgToShow = font_style.render(msg, True, color)
    screen.blit(msgToShow, [width / 4, height / 2])


class Box():  # hedefe gidecek olan nesne => mavi kutu

    x = 0
    y = 0
    w = 0

    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def MoveTo(self, x, y):
        self.x = x
        self.y = y

    def Show(self):
        pygame.draw.rect(screen, blue, [self.x, self.y, self.w, self.w])


class Trap():  # hedefe giderken yoldaki engellerin her biri => beyaz kutular

    x = 0
    y = 0
    w = 0

    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def Show(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.w, self.w])


class Terminal():  # gidilecek yer => kırmızı kutu

    x = 0
    y = 0
    w = 0

    def __init__(self, w):
        self.x = width - w
        self.y = height - w
        self.w = w

    def Show(self):
        pygame.draw.rect(screen, red, [self.x, self.y, self.w, self.w])


class Program():
    alfa = 0  # atamasi en alt kisima birakildi
    discountFactor = 0  # atamasi en alt kisima birakildi
    iteration = 0  # atamasi en alt kisima birakildi
    rows = 10
    cols = 10
    reward = 100
    qTable = []
    rTable = []
    isStarted = False
    genCount = 1
    traps = []  # engeller listesi

    def __init__(self, alfa, discountFactor, iteration):
        self.alfa = alfa
        self.discountFactor = discountFactor
        self.iteration = iteration

    # Engellerin rastgele koyulması
    def SetTraps(self):
        for value in self.rTable:
            self.rTable[random.randrange(0, self.rows - 1)][random.randrange(0, self.cols - 1)] = -1

    # Q ve R tablosu
    def SetInitsForTables(self):
        # R Tablosu ilk atamaları
        for i in range(self.rows):
            self.rTable.append([])
            for j in range(self.cols):
                if i == self.rows - 1 & j == self.cols - 1:
                    self.rTable[i].append(self.reward)
                else:
                    self.rTable[i].append(0)
        self.SetTraps()

        # Q Tablosu ilk atamaları
        for i in range(self.rows):
            self.qTable.append([])
            for j in range(self.cols):
                self.qTable[i].append(0)

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

    # Uygun yolları belirler
    def FindRoutes(self, x, y):
        routes = []
        routesWithNonNegativeVals = []
        trapList = []

        # 4 yön seçeneği
        routes.append([x - 1, y])
        routes.append([x, y - 1])
        routes.append([x + 1, y])
        routes.append([x, y + 1])

        # routesWithNonNegativeVals => gidilecek rotalardan oyun ekranından çıkaran durumlar silindi
        for route in routes:
            if route[0] > -1 and route[1] > -1:
                routesWithNonNegativeVals.append(route)

        # trapList => engeller listede tutuldu
        for trap in self.traps:
            trapList.append([trap.x / boxSize, trap.y / boxSize])

        # olası rotalardan engel noktaları silindi
        diff = [value for value in routesWithNonNegativeVals if value not in trapList]

        # diff => mavi kutucuğun gidebileceği yollar
        return diff

    # bitiş koşulu
    def IsEnd(self):
        if self.genCount == self.iteration:
            return True
        else:
            return False

    # çevresindeki Q değerlerinin hepsinin 0 olup olmadığını kontrol eder
    def isAllSame(self, qValues):
        q0 = qValues[0]
        qEqual = True

        # herhangi bir elemani farklı ise false döndür
        for qItem in qValues:
            if q0 != qItem:
                qEqual = False
                break

        return qEqual

    def Loop(self):
        # box => hareket edecek olan nesne
        # terminal => ulaşılması gereken yer
        box = Box(150, 150, boxSize)
        terminal = Terminal(boxSize)

        # traps => engellerin listeye eklenmesi
        for idx, i in enumerate(simulation.rTable):
            for idj, j in enumerate(i):
                if j == -1:
                    self.traps.append(Trap(idx * boxSize, idj * boxSize, boxSize))

        while not self.isStarted:
            if self.genCount == self.iteration:
                message('reached to max genCount', black)
                pygame.display.update()

            else:
                screen.fill(green)
                box.Show()
                terminal.Show()
                for trap in self.traps:
                    trap.Show()

                # routes => kutunun bulunduğu noktadan 4 farklı yöne gidebileceği yerler
                routes = self.FindRoutes(box.x / boxSize, box.y / boxSize)

                # qValues => gidebilinen yerlerin Q değerleri
                qValues = self.CalculateQValues(routes)

                # maxQValueIndex => seçilecek yerin Q bilgisi
                maxQValueIndex = 0

                # random farklı yönleri seçmesi için
                if self.isAllSame(qValues) == True:
                    maxQValueIndex = random.randrange(0, len(qValues))
                else:
                    maxNextQValueIndex = qValues.index(max(qValues))

                # gitmesi kararlaştırılmış yerden sonraki gidilebilecek yerler için rotalar, q değerleri, q indisi
                routesForNext = self.FindRoutes(routes[maxQValueIndex][0], routes[maxQValueIndex][1])
                qValuesForNext = self.CalculateQValues(routesForNext)
                maxNextQValueIndex = qValuesForNext.index(max(qValuesForNext))

                qX = box.x / boxSize
                qY = box.y / boxSize

                # Q değerlerinin güncellenmesi
                rValue = self.rTable[routes[maxQValueIndex][0]][routes[maxQValueIndex][1]]
                formula = self.alfa * (
                        rValue + self.discountFactor *
                        self.qTable[routes[maxNextQValueIndex][0]][routes[maxNextQValueIndex][1]])

                self.qTable[qX][qY] = self.qTable[qX][qY] + formula

                # mavi kutunun yer değiştirmesi
                box.MoveTo(routes[maxQValueIndex][0] * boxSize, routes[maxQValueIndex][1] * boxSize)

                # kırmızı noktaya ulaşma durumu
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

            # oyun frame hizi
            clock.tick(14)


# özgür can altınok
# Q learning ile gidilecek nokta için yol arama örneği

# mavi kutu => kırmızı kutuya ulaşması beklenen kutu
# beyaz kutular => engeller
# kırmızı kutu => hedef nokta, jenerasyonu yeniler
# pygame oyun motoru paketi ve random paketi kullanılmıştır

alfa = 0.5
discountFactor = 0.8
iteration = 100

simulation = Program(alfa, discountFactor, iteration)
simulation.SetInitsForTables()
simulation.Loop()

pygame.quit()
quit()
