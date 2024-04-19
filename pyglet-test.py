import pyglet
from pyglet import window
import random

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.set_location(25, 25)
        self.personagem = pyglet.shapes.Triangle(20, 20, 35, 50, 50, 20, color=(255, 0, 0), batch=self.batch)
        self.controle = {'LEFT': False, 'RIGHT': False}
        self.velocidade = 5
        self.tiros = []
        self.inimigos = []
        self.inimigo_velocidade = 2

        
    def create_tiro(self):
        tiro = pyglet.shapes.Circle(self.personagem.x + 25, self.personagem.y + 50, 5, color=(0, 0, 255), batch=self.batch)
        self.tiros.append(tiro)
    
    def create_inimigo(self):
        inimigo = pyglet.resource.image('/monstro.png')
        inimigo.x = random.randint(30, 470)
        inimigo.y = 800
        self.inimigos.append(inimigo)
        
    

    def on_draw(self):
        self.clear()
        self.batch.draw()
    


    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            self.controle['LEFT'] = True
        if symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            self.controle['RIGHT'] = True
        if symbol == pyglet.window.key.SPACE:
            self.create_tiro()

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            self.controle['LEFT'] = False
        if symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            self.controle['RIGHT'] = False

    def update(self, dt):
        if self.controle['LEFT']:
            self.personagem.x -= self.velocidade
        if self.controle['RIGHT']:
            self.personagem.x += self.velocidade
        if self.tiros:
            for tiro in self.tiros:
                tiro.y += 5
                if tiro.y > 600:
                    tiro.delete()
                    self.tiros.remove(tiro)
        if random.randint(0, 100) == 0:
            self.create_inimigo()
        if self.inimigos:
            for inimigo in self.inimigos:
                inimigo.y -= self.inimigo_velocidade
                if inimigo.y < 0:
                    inimigo.delete()
                    self.inimigos.remove(inimigo)

window = MyWindow(500, 800, 'My Window', resizable=True)
    
pyglet.clock.schedule_interval(window.update, 1/60)
pyglet.app.run()
