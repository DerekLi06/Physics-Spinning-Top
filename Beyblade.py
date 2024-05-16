from vpython import *
scene = canvas(width=800, height=800)

beyblade = cone(pos=vec(0,0,0))

#Rotates beyblade to a side view
beyblade.rotate(axis=vec(0,0,1),angle=-pi/2)

t=0; dt=3600
leave = True

def leaveLoop():
    global leave 
    leave = not(leave)

endButton = button(bind=leaveLoop,text="Click me to stop rotating!")

while (leave):
    # beyblade.rotate(axis=vec(0,1,0),angle=)
    rate(1000)

