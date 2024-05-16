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
t=0; dt=0.5
leave = True
# arrow(pos=vec(0,0,0),axis=vec(0,0,1),color=color.orange)
def leaveLoop():
    global leave 
    leave = not(leave)
beyblade.omega = 0*vector(0,0,0)

endButton = button(bind=leaveLoop,text="Click me to stop rotating!")
force_vector = arrow(pos=vec(0,0,-1))
while (t<100 or leave):
    rate(1)
    force = vector(0,0,cos(t))
    force_location = vector(0,0,radius)
    # Update force visual.
    force_vector.pos = force_location + vector(0,0,.5)
    force_vector.axis=force
    # Calculate torque.
    torque = cross(force_location,force)
    # Use update procedure.
    beyblade.omega = beyblade.omega + torque/I*dt
    beyblade.rotate(angle=mag(beyblade.omega)*dt,axis=vec(0,1,0))
    # Update time
    t = t + dt
    # beyblade.rotate(axis=vec(0,1,0),angle=pi/4)


