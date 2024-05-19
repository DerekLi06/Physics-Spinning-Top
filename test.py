from vpython import *
scene = canvas(width=800, height=800)
radius = 1
e3  = vector(1,1,1)

t = 0;dt = .5
while (t<100):
    rate(1)
    t=t+dt
    e3  = vector(1,1,1)
