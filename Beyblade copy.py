from vpython import *
scene = canvas(width=800, height=800)
radius = 1
e3  = vector(1,1,1)
theta = atan(e3.y/e3.x)
length = 1
Istar=1.2
r=length*mag(e3)

# top = cylinder(pos=vec(0.2,-0.2,0), axis=vec(0,1,0), size=vec(0.5,0.2,0.2), color=color.hsv_to_rgb(vector(0.5,1,0.8)))

#Rotates beyblade to a side view
# spin = compound([beyblade, top])
# top.rotate(axis=vec(0,0,1), angle=-pi/2)

#Constants
g=1
M = 1
Rcm = (3/4) * length #Center of Mass
I_star = (3/20.) * M *(radius**2.+4.*length**2) #Moment of Inertia along X, Y
I_33 = (.3*M*length**2.) #Moment of Inertia along Z

L3 = I_33*20 #Constant Angular Momentum
Lz = L3*cos(theta) + .5
Energy = (.5*I_star* ((Lz-L3*cos(theta))/(I_star*sin(theta)))**2 + (L3**2/ (2*I_33)) + M*g*Rcm*cos(theta)) * Istar

phi_dot = float((Lz-L3*cos(theta))/ (I_star*sin(theta)**2))
theta_dot = 0
phi = 2

beyblade = cone(pos=vector(r*sin(theta)*sin(phi),r*cos(theta),r*sin(theta)*cos(phi)),
                axis=-e3, make_trail = True,
                radius=radius, color=color.hsv_to_rgb(vector(0.5,1,0.8)),length=length)
# beyblade.trail_object.color = color.blue
# beyblade.rotate(axis=vec(0,0,1),angle=-pi/2)


# friction = 0
# I = 3 * M * (radius**2) /10
# α = 0
# ω = 0
# L = I*ω
t=0; dt=0.0000005
leave = True
# arrow(pos=vec(0,0,0),axis=vec(0,0,1),color=color.orange)
def leaveLoop():
    global leave 
    leave = not(leave)
beyblade.omega = 0*vector(0,0,0)

endButton = button(bind=leaveLoop,text="Click me to stop rotating!")
# force_vector = arrow(pos=vec(0,0,-1))
# force = vector(0,0,-1)

while (t<200):
    # spin.rotate(axis=vec(0,1,0),angle=pi/360)
    rate(250)
    t = t+dt
    theta_store = theta
    theta = theta+theta_dot*dt
    if (Energy- (.5*L3**2)/I_33 - g*M*Rcm*cos(theta)-((Lz-L3*cos(theta))/(I_star*sin(theta)))**2) < 0:
        theta = theta_store
        theta_dot = -theta_dot
    else:
        theta_dot = theta_dot + sqrt(2/I_star)*sqrt((Energy-(.5*L3**2)/I_33-g*M*Rcm*cos(theta)-((Lz-L3*cos(theta)))))
        phi_dot = phi_dot+(Lz-L3*cos(theta))/(I_star*sin(theta)**2)*dt
        phi = phi+phi_dot*dt
    beyblade.rotate(angle=pi/3, axis=beyblade.axis, origin=beyblade.pos)
    beyblade.pos = vector(r*sin(theta)*sin(phi),r*cos(theta),r*sin(theta)*cos(phi))
    beyblade.axis=-beyblade.pos

    # force = vector(0,0,cos(t))
    # force_location = vector(0,0,radius)
    # # Update force visual.
    # force_vector.pos = force_location + vector(0,0,.5)
    # force_vector.axis=force
    # # Calculate torque.
    # torque = cross(force_location,force)
    # # Use update procedure.
    # beyblade.omega = beyblade.omega + torque/I*dt
    # beyblade.rotate(angle=mag(beyblade.omega)*dt,axis=vec(0,1,0))
    # # Update time
    # t = t + dt
    # # beyblade.rotate(axis=vec(0,1,0),angle=pi/4)


