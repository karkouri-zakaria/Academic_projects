import turtle
import time
from colordict import ColorDict
 
t = turtle.Turtle()
for j,i in ColorDict().items():
  t.fillcolor(i[0]/255,i[1]/255,i[2]/255)
  t.begin_fill()
  for k in range(2):
    t.forward(200)
    t.right(90)
  t.write(j, font=("Verdana",15, "normal"))
  t.end_fill()
  time.sleep(.2)
  t.clear()