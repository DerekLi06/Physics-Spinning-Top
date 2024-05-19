from vpython import *

scene = canvas(width=800, height=800)
radius = 1
length = 1
yaxis = arrow(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.green)

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

damping_omega = 0.9995  # damping for spin
damping_omega_prec = 0.999  # damping for precession

def leaveLoop():
    global leave 
    leave = not leave

endButton = button(bind=leaveLoop, text="Click me to stop rotating!")
tilt_angle = pi / 6

beyblade.rotate(angle=tilt_angle, origin=vector(0,0.01,0),axis=vector(0,0,1))

# earrow to visualize the current axis of the beyblade
earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)

initial_angle_diff = diff_angle(vector(0,1,0), beyblade.axis)
print("Initial angle difference:", degrees(initial_angle_diff))
tilt_factor = .0005
while leave:
    rate(50)
    # Spin the beyblade about its own axis
    beyblade.rotate(angle=ω * dt, axis=beyblade.axis,origin=beyblade.pos)
    # Precession: rotate the axis of the beyblade around the vertical y-axis
    # beyblade.axis = rotate(beyblade.axis, angle=OMEGA * dt, axis=vec(0, 1, 0))
    beyblade.rotate(angle=OMEGA*dt,origin=vector(0,0,0),axis=vector(0,1,0))
    earrow.rotate(angle=OMEGA*dt,origin=vector(0,0,0),axis=vector(0,1,0))

    ω *= damping_omega
    OMEGA *= damping_omega_prec
    current_angle_diff = diff_angle(vector(0,1,0), -beyblade.axis)
    tilt_increment = 0.0005
    tilt_angle += tilt_increment
    # Rotate slightly to simulate tilting due to gravity
    beyblade.rotate(angle=tilt_increment, axis=vec(1, 0, 0))
    earrow.rotate(angle=tilt_increment, axis=vec(1, 0, 0))

    print("Current angle difference:", degrees(current_angle_diff))
    if diff_angle(vector(0,1,0),-beyblade.axis) > radians(45):
        print("top has fallen")     
        ω = 0
        OMEGA = 0
        dt = 0
        # tilt_angle = 0
        tilt_factor = 0 
    