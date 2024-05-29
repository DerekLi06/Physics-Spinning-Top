from vpython import *

scene = canvas(width=800, height=800)
radius = 0.5
length = 1
yaxis = arrow(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.green, shaftwidth=0.05)

beyblade = cone(pos=vec(0, length, 0), axis=vec(0, -1, 0), length=length, radius=radius, texture=textures.granite)

g = 9.81
M = 1
dt = 0.005
leave = True

tilt_angle = pi / 4  # Initial tilt angle

beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(1, 0, 0))

earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)
path = curve(color=color.yellow, radius=0.005)  # Initialize the path curve
Lhat = norm(beyblade.axis)
# Moments of inertia
I0 = 0.5 * M * radius ** 2  # Moment of inertia around the spinning axis
I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20  # Moment of inertia around the perpendicular axis

# Angular velocities
omega0 = 2.25 * pi  # Spin rate around its own axis
L = I0 * omega0  # Angular momentum around its own axis

def calculate_precession_rate(L, a, tilt_angle):
    return M * g * a * cos(tilt_angle) / L

def calculate_nutation_rate(L, I_perp):
    return L / I_perp

def leaveLoop():
    global leave
    leave = not leave

endButton = button(bind=leaveLoop, text="Click me to stop rotating!")

a = 3 / 4 * length
initial_angle_diff = diff_angle(vector(0, -1, 0), beyblade.axis)  # Correct axis orientation
rotated_angle = 0

while leave:
    rate(100)

    # Spin the beyblade around its own axis
    beyblade.rotate(angle=omega0 * dt, axis=beyblade.axis, origin=beyblade.pos)

    # Calculate precession angular velocity
    omega_pr = calculate_precession_rate(L, a, initial_angle_diff)
    
    # Apply precession
    beyblade.rotate(angle=omega_pr * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
    Lhat.rotate(angle=omega_pr * dt, axis=vector(0, 1, 0))
    earrow.rotate(angle=omega_pr * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
    rotated_angle += omega_pr * dt

    # Calculate nutation angular velocity
    nutation_rate = calculate_nutation_rate(L, I_perp)
    
    # Apply nutation
    nutation_axis = cross(-Lhat, vec(0, 1, 0)).norm()  # Correct nutation axis orthogonal to both spin and precession
    nutation_angle = nutation_rate * dt * sin(rotated_angle)
    beyblade.rotate(angle=nutation_angle, origin=vector(0, 0, 0), axis=nutation_axis)

    # Update angular momentum
    L = I0 * omega0

    # Trace the path of the top's axis slightly above the actual axis
    path.append(pos=-beyblade.axis * 1.5)
    
    # Keep the path temporary
    if path.npoints > 50:  # Adjust the number of points for the temporary path
        path.pop(0)

    print("Current angle difference:", degrees(diff_angle(vector(0, -1, 0), beyblade.axis)))  # Correct axis orientation
    # if diff_angle(vector(0, -1, 0), beyblade.axis) > radians(63):  # Correct axis orientation
    #     print("Top has fallen")
    #     break
