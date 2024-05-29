from vpython import *

scene = canvas(width=800, height=800)
radius = 0.5
length = 1
yaxis = arrow(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.green, shaftwidth=0.05)

beyblade = cone(pos=vec(0, length, 0), axis=vec(0, -1, 0), length=length, radius=radius, texture=textures.granite)

g = 9.81
M = 1
wr = 5*pi  # Spin rate around its own axis
dt = 0.005
leave = True

#slider for mass
def mass_set(initial):
    global mass
    mass = initial.value
    mass_caption.text = 'mass = '+'{:1.2f}'.format(my_mass.value) + "\n\n"
my_mass = slider(bind = mass_set, min = 1, max = 5, step = 0.1, value = M)
mass_caption = wtext(text = 'mass = '+'{:1.2f}'.format(my_mass.value) + "\n\n")

#slider for initial wr
def wr_set(initial):
    global wr
    wr = initial.value
    wr_caption.text = 'wr = '+'{:1.2f}'.format(my_wr.value) + "\n\n" #radians
my_wr = slider(bind = wr_set, min = 0, max = 30*pi, step = 0.1, value = wr) 
wr_caption = wtext(text = 'wr = '+'{:1.2f}'.format(my_wr.value) + "\n\n") #radians

initial_angle_diff = diff_angle(vector(0, 1, 0), beyblade.axis)
rotated_angle = 0

opp_force = 1 #temp variable to represent opposing force

COM = vector(0, 0, 0)
tilt_angle = pi / 18  # Smaller initial tilt angle

#slider for initial tilt angle
def tilt_set(initial):
    global tilt_angle
    tilt_angle = initial.value
    tilt_caption.text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "\n\n" #degrees
my_tilt = slider(bind = tilt_set, min = pi/360, max = pi/2, step = pi/360, value = tilt_angle)
tilt_caption = wtext(text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "\n\n") #degress

scene.pause()

beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(1, 0, 0))
COM = -beyblade.axis * 3 / 4
# COM_line = curve(pos=[vector(COM.x, 0, COM.z), vec(COM.x, 2, COM.z)], color=color.white)

earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)

Ir = 3 * M * radius ** 2 / 10  # Moment of inertia around the spinning axis
Ip = 3 * M * (radius ** 2 + 4 * length ** 2) / 20  # Moment of inertia around the perpendicular axis

Lr = Ir * wr  # Angular momentum around its own axis

def calculate_torque(angle_diff):
    return M * g * (3 / 4 * length) * sin(angle_diff)

def calculate_wp(torque, Lr, angle_diff):
    if Lr * sin(angle_diff) != 0:
        return torque / (Lr * sin(angle_diff))
    else:
        return 0

def calculate_opp(angle_diff):
    return opp_force * cos(angle_diff)

def leaveLoop():
    global leave
    leave = not leave

endButton = button(bind=leaveLoop, text="Click me to stop rotating!")

while leave:
    rate(50)

    beyblade.rotate(angle=wr * dt, axis=beyblade.axis, origin=beyblade.pos)

    current_angle_diff = diff_angle(vector(0, 1, 0), -beyblade.axis)
    torque = calculate_torque(current_angle_diff)
    wp = calculate_wp(torque, Lr, current_angle_diff)
    opp_torque = calculate_opp(current_angle_diff) #temp variable to represent opposing torque

    beyblade.rotate(angle=wp * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
    earrow.rotate(angle=wp * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
    rotated_angle += wp * dt

    # Update angular velocity + momentum
    if (wr > 0):
        wr = wr - opp_torque*dt    
    Lr = Ir * wr

    # Introduce nutation by slightly perturbing the tilt angle
    if(wr < 0):
        nutation_angle = 0.005 * sin(rotated_angle)  # Small oscillation
        beyblade.rotate(angle=nutation_angle, origin=vector(0, 0, 0), axis=vector(1, 0, 0))
        earrow.rotate(angle=nutation_angle, origin=vector(0,0,0), axis=vector(1,0,0))

    print("Current wr: ", wr)
    # print("Current angle difference:", degrees(current_angle_diff))
    if diff_angle(vector(0, 1, 0), -beyblade.axis) > radians(63):
        print("Top has fallen")
        break