import pyglet
from pyglet import window
from math import sin

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.personagem = pyglet.shapes.Triangle(20, 20, 45, 70, 70, 20, color=(255, 0, 0), batch=self.batch)
        self.tiro = pyglet.shapes.Circle(0, 0, 5, color=(0, 0, 255), batch=self.batch)
        self.tiro.visible = False
        self.controle = {'LEFT': False, 'RIGHT': False, 'SPACE': False}
        self.velocidade = 5

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            self.controle['LEFT'] = True
        if symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            self.controle['RIGHT'] = True
        if symbol == pyglet.window.key.SPACE:
            self.tiro.x = self.personagem.x + 25
            self.tiro.y = self.personagem.y + 50
            self.tiro.visible = True

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
        if self.tiro.visible:
            self.tiro.y += 5
            if self.tiro.y > 600:
                self.tiro.visible = False
                self.controle['SPACE'] = False

window = MyWindow(800, 600, 'My Window', resizable=True)
    
pyglet.clock.schedule_interval(window.update, 1/60)
pyglet.app.run()
