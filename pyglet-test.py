import pyglet
from pyglet import window

win = window.Window(800, 600, "Pyglet Test", resizable=True)
win.set_minimum_size(400, 300)

win.clear()

pyglet.app.run()
