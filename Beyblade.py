from vpython import *
scene = canvas(width=800, height=800)
radius = 1
beyblade = cone(pos=vec(0,0,0),radius=radius)

#Rotates beyblade to a side view
beyblade.rotate(axis=vec(0,0,1),angle=-pi/2)

g=9.81
M = 1
theta = pi
PE = 0
KE = 0
friction = 0
I = 3 * M * (radius**2) /10
α = 0
ω = 0
L = I*ω
t=0; dt=3600
leave = True

def leaveLoop():
    global leave 
    leave = not(leave)

endButton = button(bind=leaveLoop,text="Click me to stop rotating!")

while (leave):
    beyblade.rotate(axis=vec(0,1,0),angle=pi/4)
    rate(1)

