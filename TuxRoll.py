#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#       TuxRoll.py
#
#       Copyright 2010
#       David Litvak <davidlitvak.b@gmail.com>
#       Sebastian Alonso <alon.sebastian@gmail.com>
#       Martin Volpe <volpe.martin@gmail.com>
#       Alina Godino <alina@fibertel.com.ar> {Diseño Grafico}
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pygame
from random import randrange

#Inicializar pygame
print 'Bienvenido a TuxRoll+\n\n\n\n\n\n\n\n'
raw_input('Presione Enter para comenzar a jugar\n\n\n\n\n')

pygame.init()
pygame.font.init()
SIZE = (450, 550)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("TuxRoll+")

#Cargar recursos
fondo = pygame.image.load("images/imagenDeFondo.jpg").convert_alpha()
font = pygame.font.Font(None,32)
musicaFondo = pygame.mixer.Sound("sound/mision.ogg")
musicaFondo.play(0)


#Lo comentado debajo... funciona como si Tux fuera un paraguas
class Tux(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
#      self.imagenBack = pygame.image.load("images/blanco.png")
      self.image = pygame.image.load("images/tux.png")
#      self.rect = self.imagenBack.get_rect()
      self.rect = self.image.get_rect()
      self.rect[1] = 25
      self.rect[0] = 200

    def movs(self,dx):
      self.rect.move_ip([dx,0])
      self.rect.clamp_ip(screen.get_rect())

class Barra(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.rect = self.image.get_rect()
      self.rect.clamp_ip(screen.get_rect())
      self.rect[1] = 550
      self.rect[0] = randrange(-75,405)
    def update(self):
      self.rect[1] -= 3

class Corazon(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("images/corazon.png")
      self.rect = self.image.get_rect()
      self.rect.clamp_ip(screen.get_rect())
      self.rect[1] = 550
      self.rect[0] = randrange(405)
    def update(self):
      self.rect[1] -= 3

class BarraBuena(Barra):
    image = pygame.image.load("images/barra.png").convert_alpha()

class BarraMala(Barra):
    image = pygame.image.load("images/barraMala.png").convert_alpha()

class BarraArriba(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("images/barraArriba.png").convert_alpha()
      self.rect = self.image.get_rect()
      self.rect.clamp_ip(screen.get_rect())
      self.rect[1] = 0

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, color=(255,255,255), format="%06d"):
      pygame.sprite.Sprite.__init__(self)
      self.color = color
      self.format = format
      self.actualizarPuntaje(0)
      self.rect[0] = 495
      self.rect[1] = 25
    def actualizarPuntaje(self,puntaje):
      self.text = self.format % puntaje
      self.image = font.render(self.text,1,self.color)
      self.rect = self.image.get_rect()
      self.rect[0] = 450 - self.rect[3] - 65
      self.rect[1] = 25

class DisplayNivel(pygame.sprite.Sprite):
    def __init__(self, color=(255,255,255), format="%s %d"):
      pygame.sprite.Sprite.__init__(self)
      self.color = color
      self.format = format
      self.actualizarNivel(0)
      self.rect[1] = 25
    def actualizarNivel(self,nivelDisplay):
      self.text = self.format % ('Nivel ',nivelDisplay)
      self.image = font.render(self.text,1,self.color)
      self.rect = self.image.get_rect()
      self.rect[1] = 25

class DisplayVidas(pygame.sprite.Sprite):
    def __init__(self, color=(255,255,255), format="%s %d"):
      pygame.sprite.Sprite.__init__(self)
      self.color = color
      self.format = format
      self.actualizarVidas(3)
      self.rect[0] = 200
      self.rect[1] = 25
    def actualizarVidas(self,vidas):
      self.text = self.format % ('Vidas ',vidas)
      self.image = font.render(self.text,1,self.color)
      self.rect = self.image.get_rect()
      self.rect[0] = 200
      self.rect[1] = 25

#Inicializar simulacion
screen.blit(fondo,(0,0))
clock = pygame.time.Clock()
tux = Tux()
grupoTux = pygame.sprite.Group()
grupoTux.add(tux)

barraArriba = BarraArriba()
grupoBarraArriba = pygame.sprite.Group()
grupoBarraArriba.add(barraArriba)

grupoBarraBuena = pygame.sprite.Group()
grupoBarraMala = pygame.sprite.Group()

grupoCorazon = pygame.sprite.Group()

proximaBarra = 0
dificultadMaxima = 100
dificultadBarras = 20

score = ScoreBoard()
grupoScoreBoard = pygame.sprite.Group()
grupoScoreBoard.add(score)

displayNivel = DisplayNivel()
grupoDisplayNivel = pygame.sprite.Group()
grupoDisplayNivel.add(displayNivel)

displayVidas = DisplayVidas()
grupoDisplayVidas = pygame.sprite.Group()
grupoDisplayVidas.add(displayVidas)

contador = 0
nivel = 30
nivelDisplay = 0
puntaje = 0
vidas = 3
corazones = randrange(30,500)

running = True
#Repetir:
while running:
    #   1-Procesar acciones del jugador
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        tux.movs(-10)
    elif keystate[pygame.K_RIGHT]:
        tux.movs(10)

#   2-Avanzar simulacion
    clock.tick(nivel)
    if proximaBarra < 1:
        #crear una barra nueva
        if randrange(dificultadMaxima) > dificultadBarras:
          grupoBarraBuena.add(BarraBuena())
        else:
          grupoBarraMala.add(BarraMala())
        #resetear proximaBarra
        proximaBarra = 40
    proximaBarra -= 1
    if corazones < 1:
        #crear un corazon nuevo
        grupoCorazon.add(Corazon())
        #resetear corazones
        corazones = randrange(30,500)
    corazones -= 1

    #Movimiento Tux
    if pygame.sprite.spritecollide(tux,grupoBarraBuena,dokill=False):
        tux.rect[1] -= 3
    else:
        tux.rect[1] += 5

    #Formas de perder
    if tux.rect[1] >= 545:
        vidas -= 1
        tux.rect[1] = 35
        tux.rect[0] = 200

    if pygame.sprite.spritecollide(tux,grupoBarraArriba,dokill=False):
        vidas -= 1
        tux.rect[1] = 65
        tux.rect[0] = 200

    if pygame.sprite.spritecollide(tux,grupoBarraMala,dokill=True):
        vidas -= 1
        tux.rect[1] = 35
        tux.rect[0] = 200

    #Quitar Corazones de memoria
    if pygame.sprite.spritecollide(barraArriba,grupoCorazon,dokill=True):
        pass

    #Puntos!
    if pygame.sprite.spritecollide(barraArriba,grupoBarraBuena,dokill=True) or \
    pygame.sprite.spritecollide(barraArriba,grupoBarraMala,dokill=True):
        contador += 1
        if contador == (10 * (nivelDisplay + 1)):
            contador = 0
            nivel += 10
            dificultadBarras += 2
            nivelDisplay += 1
        puntaje += 10 * (nivelDisplay + 1)
    if pygame.sprite.spritecollide(tux,grupoCorazon,dokill=True):
        vidas += 1
        puntaje += 100

    score.actualizarPuntaje(puntaje)
    displayNivel.actualizarNivel(nivelDisplay)
    displayVidas.actualizarVidas(vidas)

    if dificultadBarras == dificultadMaxima:
        running = False
        print "Ganaste! No hay mas niveles"

    if vidas == 0:
        running = False
        print "Ha finalizado tu partida"

#   3-Dibujar estado actual
    grupoBarraBuena.update()
    grupoBarraMala.update()
    grupoCorazon.update()
    grupoTux.clear(screen, fondo)
    grupoTux.draw(screen)
    grupoCorazon.clear(screen, fondo)
    grupoCorazon.draw(screen)
    grupoBarraBuena.clear(screen, fondo)
    grupoBarraBuena.draw(screen)
    grupoBarraMala.clear(screen, fondo)
    grupoBarraMala.draw(screen)
    grupoBarraArriba.clear(screen, fondo)
    grupoBarraArriba.draw(screen)
    grupoScoreBoard.clear(screen, fondo)
    grupoScoreBoard.draw(screen)
    grupoDisplayNivel.clear(screen, fondo)
    grupoDisplayNivel.draw(screen)
    grupoDisplayVidas.clear(screen, fondo)
    grupoDisplayVidas.draw(screen)
    pygame.display.flip()

musicaFondo.stop()


if puntaje > 10000:
  print 'Sos el maestro!'
elif puntaje > 5000 and puntaje <= 10000:
  print 'Excelente!'
elif puntaje > 3000 and puntaje <= 5000:
  print 'Muy Bien!'
elif puntaje > 1000 and puntaje <= 3000:
  print 'Bien!'
else:
  print 'Boo!'

print "Tu puntaje fue:",puntaje
pygame.quit()
