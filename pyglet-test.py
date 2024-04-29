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
        self.velocidade = 10
        self.tiros = []
        self.inimigos = []
        self.inimigo_velocidade = 2
        self.pontos = 0
        self.vidas = 3
        self.jogando = False

        
    def create_tiro(self):
        tiro = pyglet.shapes.Rectangle(self.personagem.x + 25, self.personagem.y + 50, 2, 10, color=(0, 0, 255), batch=self.batch)
        self.tiros.append(tiro)
    
    def create_inimigo(self):
        aleatorio = random.randint(0, 100)
        inimigo_selecionado = None
        if aleatorio < 50:
            invader_frames = []
            for i in range(1, 3):
                image = pyglet.resource.image('assets/invader' + str(i) + '.png')
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2
                invader_frames.append(pyglet.image.AnimationFrame(image, 0.5))
            inimigo_selecionado = pyglet.image.Animation(invader_frames)
        if aleatorio >= 50:
            monster_frames = []
            for i in range(1, 3):
                image = pyglet.resource.image('assets/monster' + str(i) + '.png')
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2
                monster_frames.append(pyglet.image.AnimationFrame(image, 0.5))
            inimigo_selecionado = pyglet.image.Animation(monster_frames)
        inimigo = pyglet.sprite.Sprite(inimigo_selecionado, x=random.randint(20, 280), y=600, batch=self.batch)
        self.inimigos.append(inimigo)
        
    def colisao(self):
        if self.inimigos and self.tiros:
            for inimigo in self.inimigos:
                for tiro in self.tiros:
                    if inimigo.x - 25 < tiro.x < inimigo.x + 25 and inimigo.y - 25 < tiro.y < inimigo.y + 25:
                        inimigo.delete()
                        tiro.delete()
                        self.inimigos.remove(inimigo)
                        self.tiros.remove(tiro)
                        self.pontos += 1
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
        self.colisao()
        print(self.inimigos)
        self.label = pyglet.text.Label(str(self.pontos), x=10, y=10, batch=self.batch)
        if self.controle['LEFT']:
            self.personagem.x -= self.velocidade
        if self.controle['RIGHT']:
            self.personagem.x += self.velocidade
        if self.personagem.x < 0:
            self.personagem.x = 0
        if self.personagem.x > 270:
            self.personagem.x = 270
        if self.tiros:
            for tiro in self.tiros:
                tiro.y += 10
                if tiro.y > 600:
                    tiro.delete()
                    self.tiros.remove(tiro)
        if random.randint(0, 100) < 4 or not self.inimigos:
            self.create_inimigo()
        if self.inimigos:
            for inimigo in self.inimigos:
                inimigo.y -= self.inimigo_velocidade
                if inimigo.y < 0:
                    inimigo.delete()
                    self.inimigos.remove(inimigo)
                    self.vidas -= 1
        if self.pontos > 10:
            self.inimigo_velocidade = 3
        if self.pontos > 25:
            self.inimigo_velocidade = 4
        if self.pontos > 50:
            self.inimigo_velocidade = 5
        if self.pontos > 100:
            self.inimigo_velocidade = 7
        if self.pontos > 150:
            self.inimigo_velocidade = 10
        if self.pontos > 200:
            self.inimigo_velocidade = 12

window = MyWindow(300, 600, 'My Window', resizable=False)

pyglet.clock.schedule_interval(window.update, 1/30)
pyglet.app.run()
