from vpython import *

scene = canvas(width=800, height=800)
radius = 1
length = 1
yaxis = arrow(pos=vec(0, length, 0), axis=vec(0, 1, 0), color=color.green)

# Initialize beyblade with a tilt
beyblade = cone(pos=vec(0, length, 0), axis=vec(0, -1, 0), length=length, radius=radius, 
                texture=textures.granite)

g = 9.81
M = 1
I = 3 * M * (radius**2) / 10
ω = 10*pi
dt = .005
leave = True
# Angular velocity of precession
OMEGA = 10 * g * length / (3 * ω * radius**2)

def leaveLoop():
    global leave 
    leave = not leave

endButton = button(bind=leaveLoop, text="Click me to stop rotating!")

beyblade.rotate(angle=pi/6, origin=vector(0,0.01,0),axis=vector(0,0,1))

# earrow to visualize the current axis of the beyblade
earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)
# earrow.rotate(angle=pi/6, origin=vector(0,0.01,0),axis=vector(0,0,1))
while leave:
    rate(100)
    # Spin the beyblade about its own axis
    beyblade.rotate(angle=ω * dt, axis=beyblade.axis,origin=beyblade.pos)
    # Precession: rotate the axis of the beyblade around the vertical y-axis
    # beyblade.axis = rotate(beyblade.axis, angle=OMEGA * dt, axis=vec(0, 1, 0))
    beyblade.rotate(angle=OMEGA*dt,origin=vector(0,0,0),axis=vector(0,1,0))
    # Update the arrow to match the new axis of the beyblade
    earrow.rotate(angle=OMEGA*dt,origin=vector(0,0,0),axis=vector(0,1,0))
    