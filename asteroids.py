from FGAme import *
from FGAme.mathutils import convex_hull, pi
from random import normalvariate, uniform

###############################################################################
#                                 Tarefas
###############################################################################
#
# Nome/matrícula:Lucas Costa Araujo / 130060313
# Nome/matrícula:Lucas Gomes Pereira / 130013242
#
# 1) Completar o reposicionamento dos asteróids nas quatro direções
#    dentro da função force_bounds()
# 2) Implementar o movimento da nave nas quatro direções dentro das funções
#    ship_left/right/front/back
# 3) Implementar parcialmente o tiro (apenas uma bolinha saindo da nave, sem
#    qualquer outro efeito). Modifique a função on_shot()

###############################################################################
#                           Constantes do jogo
###############################################################################
ASTEROIDS_COLOR = (200, 200, 200)
ASTEROIDS_SPEED = 50
ASTEROIDS_RADIUS = 20
WIDTH = 800
HEIGHT = 600
INTENSIDADE_VEL = 30

###############################################################################
#                             Implementação
###############################################################################


class Asteroids(World):

    '''Define uma fase do jogo Asteroids'''

    def __init__(self, num_asteroids=7):
        World.__init__(self, background='black')

        # Cria asteróides
        self.asteroids = [self.new_asteroid(ASTEROIDS_RADIUS, world=self)
                          for _ in range(num_asteroids)]

        # Cria a nave
        vertices = [(0, 0), (20, 0), (10, 30)]
        self.spaceship = Poly(vertices, color='red', pos=pos.middle)
        self.add(self.spaceship)

    def new_asteroid(self,
                     radius,
                     mean_speed=ASTEROIDS_SPEED,
                     color=ASTEROIDS_COLOR, **kwds):
        '''Cria um novo asteróide'''

        # Sorteadores de números aleatórios
        g = normalvariate
        r = uniform

        # Sorteia vertices
        points = [(g(0, radius), g(0, radius)) for _ in range(20)]
        points = convex_hull(points)

        # Sorteia posições e velocidades
        pos = (r(0, WIDTH), r(0, HEIGHT))
        vel = (g(0, mean_speed), g(0, mean_speed))

        # Cria um polígono
        Poly(points, vel=vel, pos=pos, color=color, **kwds)
        return Poly(points, vel=vel, pos=pos, color=color, **kwds)

    @listen('frame-enter')
    def force_bounds(self):
        '''Executado a cada frame: testa todos os asteroids para ver se saíram
        da tela. Em caso positivo, eles são recolocados do lado oposto'''

        for asteroid in self.asteroids:
            #Asteroide atravessa em cima
            if asteroid.ymin > HEIGHT:
                asteroid.move((0, -HEIGHT - asteroid.height + 1))
            #Asteriode atravessa em baixo
            if asteroid.ymax < 0: 
                asteroid.move((0, HEIGHT + asteroid.height - 1))
            #Asteroide atravessa na direita
            if asteroid.xmin > WIDTH: 
                asteroid.move((-WIDTH - asteroid.width + 1, 0))
            #Asteroide atravessa na esquerda
            if asteroid.xmax < 0:
                asteroid.move((WIDTH + asteroid.width - 1, 0))

    #Retorna o vetor unitario que indica a direcao que a nave esta orientada
    def calcula_direcao_spaceship(self):
        direcao = (self.spaceship.vertices[2] - self.spaceship.pos).normalized()
        return direcao

    @listen('long-press', 'left')
    def ship_left(self):
        self.spaceship.rotate(0.1)

    @listen('long-press', 'right')
    def ship_right(self):
       self.spaceship.rotate(-0.1)

    @listen('long-press', 'up')
    def ship_front(self):
        self.spaceship.vel += INTENSIDADE_VEL*self.calcula_direcao_spaceship()

    @listen('long-press', 'down')
    def ship_back(self):
        self.spaceship.vel += -INTENSIDADE_VEL*self.calcula_direcao_spaceship()        

    @listen('key-down', 'space')
    def on_shot(self):
        vel = self.calcula_direcao_spaceship()*100
        pos = self.spaceship.vertices[2]
        Circle(2, pos=pos, vel=vel, color='white', world=self)



if __name__ == '__main__':
    game = Asteroids()
    game.run()
