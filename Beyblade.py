from vpython import *
scene = canvas(width=800, height=800)
radius = 1
beyblade = cone(pos=vec(0,0,0),radius=radius, color=color.hsv_to_rgb(vector(0.5,1,0.8)))
top = cylinder(pos=vec(0.2,-0.2,0), axis=vec(0,1,0), size=vec(0.5,0.2,0.2), color=color.hsv_to_rgb(vector(0.5,1,0.8)))

#Rotates beyblade to a side view
beyblade.rotate(axis=vec(0,0,1),angle=-pi/2)
spin = compound([beyblade, top])
# top.rotate(axis=vec(0,0,1), angle=-pi/2)
spin.rotate(axis=vec(1,0,0), angle=-pi/90)

g=9.81
M = 1
theta = pi
PE = 0
KE = 0
friction = 0
I = 3 * M * (radius**2) /10
ω = 0
L = I*ω
t=0; dt=3600
leave = True

def leaveLoop():
    global leave 
    leave = not(leave)

endButton = button(bind=leaveLoop,text="Click me to stop rotating!")

while (leave):
    spin.rotate(axis=vec(0,1,0),angle=pi/360)
    rate(1000)

