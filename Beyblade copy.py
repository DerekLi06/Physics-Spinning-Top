from vpython import *

scene = canvas(width=600, height=400)
scene.center = vec(0, 0, 0)
scene.forward = vec(0,-0.5,-1)
# scene.camera.rotate(angle = 45, axis = vec(0,1,0))
# scene.center = vec(0, 0, 0)
radius = 0.5
length = 1
yaxis = arrow(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.green, shaftwidth=0.05)
plane = cylinder(pos=vec(0, 0, 0), axis = vec(0, 1, 0), radius=2, length = 0.01, texture=textures.earth)
light = distant_light(direction = vec(-0.5,-0.8,-0.5), color = color.white)
beyblade = cone(pos=vec(0, length, 0), axis=vec(0, -1, 0), length=length, radius=radius, texture=textures.granite)

running = True
g = 9.81
M = 1
dt = 0.005
leave = True
#angular velocity
omega0 = 5 * pi  # Spin rate around its own axis

# opposing force
uk = 0.5
fric_torq = uk * M * g * 0.004

tilt_angle = pi / 4  # Initial tilt angle

beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))

earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)
path = curve(color=color.yellow, radius=0.005)  # Initialize the path curve
Lhat = norm(beyblade.axis)
# Moments of inertia
I0 = 3 * M * radius ** 2 / 10  # Moment of inertia around the spinning axis/vertical
I_perp = (3 * M * ((radius ** 2) + (4 * length ** 2))) / 20  # Moment of inertia around the perpendicular axis/horizontal

# Angular momentum
L = I0 * omega0  # Angular momentum around its own axis

beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))

earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)
path = curve(color=color.yellow, radius=0.005)  # Initialize the path curve
Lhat = norm(beyblade.axis)
# Moments of inertia
I0 = 3 * M * radius ** 2 / 10  # Moment of inertia around the spinning axis
I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20  # Moment of inertia around the perpendicular axis

# Angular momentum
L = I0 * omega0  # Angular momentum around its own axis

#slider for mass
caption = wtext(text = "\n\t\t Modify the Top's Properties Using the Sliders Below: \n\n")
def mass_set(initial):
    global mass
    global I0
    global I_perp
    global L
    mass = initial.value
    I0 = 3 * M * radius ** 2 / 10
    I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20
    L = I0 * omega0
    mass_caption.text = 'mass = '+'{:1.2f}'.format(my_mass.value) + "kg\n\n"
my_mass = slider(bind = mass_set, min = 0.1, max = 5, step = 0.1, value = M)
mass_caption = wtext(text = 'mass = '+'{:1.2f}'.format(my_mass.value) + " kg\n\n")

#slider for initial omega0
def omega0_set(initial):
    global omega0
    global L
    omega0 = initial.value
    L = I0 * omega0
    omega0_caption.text = 'omega0 = '+'{:1.2f}'.format(my_omega0.value) + " radians \n\n" #radians
my_omega0 = slider(bind = omega0_set, min = 0, max = 10*pi, step = 0.1, value = omega0) 
omega0_caption = wtext(text = 'omega0 = '+'{:1.2f}'.format(my_omega0.value) + " radians\n\n") #radians

#slider for initial tilt angle
def tilt_set(initial):
    global tilt_angle
    global Lhat
    global beyblade
    global earrow
    tilt_angle = initial.value
    beyblade.pos = vec(0, length, 0)
    beyblade.axis = vec(0, -1, 0)
    earrow.axis = -beyblade.axis
    earrow.length = 2
    beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    earrow.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    Lhat = norm(beyblade.axis)
    tilt_caption.text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "°\n\n" #degrees
my_tilt = slider(bind = tilt_set, min = pi/360, max = pi/3, step = pi/360, value = tilt_angle)
tilt_caption = wtext(text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "°\n\n") #degress

def fric_coeff(initial):
    global uk
    global fric_torq
    uk = initial.value
    fric_torq = uk * M * g * radius
    fric_caption.text = 'friction coefficient = '+'{:1.2f}'.format(my_fric.value) + "\n\n"
my_fric = slider(bind = fric_coeff, min = 0.01, max = 2, step = 0.01, value = uk)
fric_caption = wtext(text = 'friction coefficient = '+'{:1.2f}'.format(my_fric.value) + "\n\n")

#button for locking in slider decisions
def lock():
    global my_mass
    global my_omega0
    global my_tilt
    global my_fric
    my_mass.disabled = True
    my_omega0.disabled = True
    my_tilt.disabled = True
    my_fric.disabled = True

confirm = button(bind=lock, text = "Click me to lock in your top properties!")
start = wtext(text = "\n\n\t\t\tClick in the Canvas to Start the Simulation!\n\n", visible = False)

myevnt = scene.pause()

def calculate_precession_rate(L, a, tilt_angle):
    return M * g * a * cos(tilt_angle) / L

def calculate_nutation_rate(L, I_perp):
    return L / I_perp

def leaveLoop():
    global leave
    leave = not leave

endButton = button(bind=leaveLoop, text="Click me to stop rotating!")
wtext(text = "\t\t")

#start/pause button
def run(b):
    global running
    if running:
        b.text = "Start"
    else:
        b.text = "Pause"
    running = not running

pause_start = button(bind=run, text = "Pause")

a = (3 / 4) * length
initial_angle_diff = diff_angle(vector(0, -1, 0), beyblade.axis)  # Correct axis orientation
rotated_angle = 0

#reset button
def restart():
    global running
    global M
    global omega0
    global tilt_angle
    global my_mass
    global my_omega0
    global my_tilt
    global my_fric
    global Lhat
    global I_perp
    global L
    global I0
    global uk
    global fric_torq
    beyblade.pos = vec(0,length,0)
    beyblade.axis = vec(0,-1,0)
    my_mass.disabled = False
    my_omega0.disabled = False
    my_tilt.disabled = False
    my_fric.disabled = False
    confirm.disabled = False
    M = 1
    omega0 = 5 * pi
    tilt_angle = pi / 4
    uk = 0.5
    my_mass.value = M
    mass_caption.text = 'mass = '+'{:1.2f}'.format(my_mass.value) + "kg\n\n"
    my_omega0.value = omega0
    omega0_caption.text = 'omega0 = '+'{:1.2f}'.format(my_omega0.value) + " radians \n\n" #radians
    my_tilt.value = tilt_angle
    tilt_caption.text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "°\n\n" #degrees
    my_fric.value = uk
    fric_caption.text = 'friction coefficient = '+'{:1.2f}'.format(my_fric.value) + "\n\n"
    for i in range(50):
        path.pop(0)
    beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    earrow.axis = -beyblade.axis
    earrow.length = 2
    Lhat = norm(beyblade.axis)
    I0 = 3 * M * radius ** 2 / 10 
    I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20 
    L = I0 * omega0 
    fric_torq = uk * M * g * radius
    endButton.disabled = True
    reset.disabled = True
    pause_start.disabled = True
    running = False
    scene.pause()
    running = True
    confirm.disabled = True
    my_mass.disabled = True
    my_omega0.disabled = True
    my_tilt.disabled = True
    my_fric.disabled = True
    endButton.disabled = False
    reset.disabled = False
    pause_start.disabled = False
    running = True
    
wtext(text = "\t\t")
reset = button(bind = restart, text = "Reset")
wtext(text = "\n\n")

confirm.disabled = True
my_mass.disabled = True
my_omega0.disabled = True
my_tilt.disabled = True
my_fric.disabled = True

while leave:
    time += dt
    rate(50)
    if running:
        scene.camera.rotate(angle = 0.01, axis = vec(0,1,0))
        scene.center = vec(0, 0, 0)

        # Spin the beyblade around its own axis
        beyblade.rotate(angle=omega0 * dt, axis=beyblade.axis, origin=beyblade.pos)

        # Calculate precession angular velocity
        omega_pr = calculate_precession_rate(L, a, initial_angle_diff)
        
        # Apply precession
        beyblade.rotate(angle=omega_pr * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
        Lhat.rotate(angle=omega_pr * dt, axis=vector(0, 1, 0))
        earrow.rotate(angle=omega_pr * dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
        rotated_angle += omega_pr * dt * 5

        # Calculate nutation angular velocity
        nutation_rate = calculate_nutation_rate(L, I_perp)
    
        # Apply nutation
        nutation_axis = cross(-Lhat, vec(0, 1, 0)).norm()  # Correct nutation axis orthogonal to both spin and precession
        nutation_angle = nutation_rate * dt * sin(rotated_angle)
        print("nutation angle: ",nutation_angle)

        beyblade.rotate(angle=nutation_angle, origin=vector(0, 0, 0), axis=nutation_axis)
    
        # Update angular momentum
        if(omega0 > 0):
            omega0 = omega0 - fric_torq*dt
        L = I0 * omega0
    
        # Trace the path of the top's axis slightly above the actual axis
        path.append(pos=-beyblade.axis * 1.5)
        
        # Keep the path temporary
        if path.npoints > 50:  # Adjust the number of points for the temporary path
            path.pop(0)
    
        print("Current angle difference:", degrees(diff_angle(vector(0, -1, 0), beyblade.axis)))  # Correct axis orientation
        if diff_angle(vector(0, -1, 0), beyblade.axis) > radians(69):  # Correct axis orientation
            print("Top has fallen")
            break
