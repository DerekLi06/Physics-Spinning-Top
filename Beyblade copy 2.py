from vpython import *

scene = canvas(width=600, height=400)
scene.center = vec(0, 0, 0)
scene.forward = vec(0,-0.5,-1)
# scene.camera.rotate(angle = 45, axis = vec(0,1,0))
# scene.center = vec(0, 0, 0)
radius = 1
length = .9
yaxis = arrow(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.green, shaftwidth=0.05)
plane = cylinder(pos=vec(0, 0, 0), axis = vec(0, 1, 0), radius=2, length = 0.01, texture=textures.earth)
light = distant_light(direction = vec(-0.5,-0.8,-0.5), color = color.white)
beyblade = cone(pos=vec(0, 1, 0), axis=vec(0, -1, 0), length=1, radius=radius/2, texture=textures.granite)
nutation_arrow = arrow(pos=vec(0, 0, 0), axis=vec(1, 0, 0), color=color.blue, shaftwidth=0.03)

running = True
g = 9.81
M = 10
dt = 0.005
leave = True
#angular velocity
omega0 = 3 * pi  # Spin rate around its own axis
theta = diff_angle(vector(0, 1, 0), -beyblade.axis)
print("theta1 ",theta)
tilt_angle = pi/6 +.00001  # Initial tilt angle
beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
theta = diff_angle(vector(0, 1, 0), -beyblade.axis)
print("theta2 ",degrees(theta))
earrow = arrow(length=2, axis=-beyblade.axis, color=color.red, shaftwidth=0.007)
path = curve(color=color.yellow, radius=0.005)  # Initialize the path curve
Lhat = norm(beyblade.axis)
# Moments of inertia
I0 = 3 * M * radius ** 2 / 10  # Moment of inertia around the spinning axis
I_perp = (3 * M * (radius ** 2 + 4 * (length*3/4) ** 2)) / 20  # Moment of inertia around the perpendicular axis
print("I0: ",I0)
print("I_perp: ",I_perp)
# Angular momentum
L = I0 * omega0  # Angular momentum around its own axis


#slider for mass
caption = wtext(text = "\n\t\t Modify the Top's Properties Using the Sliders Below: \n\n")
def mass_set(initial):
    global mass
    global I0
    global I_prep
    global L
    mass = initial.value
    I0 = 3 * M * radius ** 2 / 10
    I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20
    L = I0 * omega0
    mass_caption.text = 'mass = '+'{:1.2f}'.format(my_mass.value) + "\n\n"
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
    tilt_caption.text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + "\n\n" #degrees
my_tilt = slider(bind = tilt_set, min = pi/360, max = pi/3, step = pi/360, value = tilt_angle)
tilt_caption = wtext(text = 'initial tilt = '+'{:1.2f}'.format(degrees(my_tilt.value)) + " kg\n\n") #degress

#button for locking in slider decisions
def lock():
    global my_mass
    global my_omega0
    global my_tilt
    my_mass.disabled = True
    my_omega0.disabled = True
    my_tilt.disabled = True

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

def calculate_beta(alpha, M, r, l):
    I0 = 3 * M * r ** 2 / 10
    I_perp = 3 * M * (r ** 2 + 4 * (3 / 4 * l) ** 2) / 20
    beta = asin(sin(alpha) * (I_perp / I0))
    return beta

a = (3 / 4) * length
initial_angle_diff = diff_angle(vector(0, -1, 0), beyblade.axis)  # Correct axis orientation
rotated_angle = 0
omega_pr = calculate_precession_rate(L, a, initial_angle_diff)
Lz = L*cos(tilt_angle)
Energy = ((Lz-L*cos(tilt_angle))**2 / (2*I_perp*(sin(tilt_angle)**2))) + (L**2 / (2*I0)) + (M*g*a*cos(tilt_angle))
print("Energy: ",Energy)
print("L3: ",L)
print("Lz: ",Lz)
#reset button
def restart():
    global running
    global M
    global omega0
    global tilt_angle
    global my_mass
    global my_omega0
    global L
    global I_perp
    global Lhat
    global my_tilt
    beyblade.pos = vec(0,length,0)
    beyblade.axis = vec(0,-1,0)
    my_mass.disabled = False
    my_omega0.disabled = False
    my_tilt.disabled = False
    confirm.disabled = False
    M = 1
    omega0 = 5 * pi
    tilt_angle = pi / 4
    my_mass.value = M
    my_omega0.value = omega0
    my_tilt.value = tilt_angle
    for i in range(50):
        path.pop(0)
    beyblade.rotate(angle=tilt_angle, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    earrow.axis = -beyblade.axis
    earrow.length = 2
    Lhat = norm(beyblade.axis)
    I0 = 3 * M * radius ** 2 / 10 
    I_perp = (3 * M * (radius ** 2 + 4 * length ** 2)) / 20 
    L = I0 * 20
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
goingDown = True
time = 0
theta_dot = 1e-3
phi_dot = float(Lz-L)

def quadraticEqSolver(a,b,c):
    d = b**2-4*a*c
    if d < 0:
        return [0]
    elif d == 0:
        return [(-b+sqrt(b**2-4*a*c))/(2*a)]
    else:
        return [(-b+sqrt(b**2-4*a*c))/(2*a), (-b-sqrt(b**2-4*a*c))/(2*a)]
print("Tielt_ angle: ",tilt_angle)
nutation_axis = cross(-Lhat, vec(0, 1, 0)).norm()  # Ensure nutation axis is perpendicular to -Lhat
beta = calculate_beta(tilt_angle,M,radius,length)
print("Beta: ",degrees(beta))
down = True
turn = 0

previous_theta_dot = theta_dot

while leave:
    rate(30)
    if running:
        # scene.camera.rotate(angle = 0.01, axis = vec(0,1,0))
        # scene.center = vec(0, 0, 0)

        # Spin the beyblade around its own axis
        beyblade.rotate(angle=omega0 * dt, axis=beyblade.axis, origin=beyblade.pos)

        # Calculate precession angular velocity
        B = 2*M*g*a/I_perp
        A = B*cos(tilt_angle)
        

        # Calculate nutation angular velocity
        nutation_rate = calculate_nutation_rate(L, I_perp)
        # a0 = A - (Lz/I_perp)**2
        a1 = 2*Lz*L/((I_perp)**2)
        a2 = -A - (L/I_perp)**2 
        bounds = quadraticEqSolver(B,a2,a1)
        # Apply nutation
        phi_dot = (Lz-L*cos(tilt_angle))/(I_perp*(sin(theta)**2))
        print("previous_theta_dot: ",previous_theta_dot)
        if (previous_theta_dot<0 and theta_dot>0):
            print("DOWN IS NOW TRUE!")
            theta_dot = 0
            down = True
        previous_theta_dot = theta_dot
        if (down and theta>=beta):
            print("I ran!")
            theta_dot = -theta_dot
            down = False
        
        elif (((2/I_perp)*(Energy-.5*I0*omega0**2-M*g*a*cos(theta)) - ((Lz-L*cos(theta)) / (I_perp*sin(theta)))**2)>=0):
           theta_dot = theta_dot+sqrt((2/I_perp)*(Energy-(.5*I0*(omega0**2))-(M*g*a*cos(theta))) - ((Lz-L*cos(theta)) / (I_perp*sin(theta)))**2)
           print("This thing equals: ",((2/I_perp)*(Energy-.5*I0*omega0**2-M*g*a*cos(theta)) - ((Lz-L*cos(theta)) / (I_perp*sin(theta)))**2))
        
        nutation_angle = theta_dot*dt
        omega_pr = omega_pr + phi_dot*dt
        # Apply precession
        print("omega_pr*dt: ",omega_pr*dt)
        beyblade.rotate(angle=omega_pr*dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))
        Lhat.rotate(angle=omega_pr*dt, axis=vector(0, 1, 0))
        earrow.rotate(angle=omega_pr*dt, origin=vector(0, 0, 0), axis=vector(0, 1, 0))

        # rotated_angle += omega_pr * dt * 5
        theta = diff_angle(vector(0, 1, 0), -beyblade.axis)
        tangent = cross(beyblade.axis, vector(0, 1, 0)).norm()
        print("nutation angle: ",nutation_angle)
        print("theta: ",degrees(theta))
        print("theta_dot: ",theta_dot)
        print("phi_dot: ",phi_dot)
        print("Current angle difference:", degrees(diff_angle(vector(0, -1, 0), beyblade.axis)))  # Correct axis orientation
        print("\n")

        beyblade.rotate(angle=nutation_angle, origin=vector(0, 0, 0), axis=tangent)
    
        nutation_arrow.pos = beyblade.pos
        nutation_arrow.axis = tangent * 2
        # Trace the path of the top's axis slightly above the actual axis
        path.append(pos=-beyblade.axis * 1.5)
        time+=dt
        if path.npoints > 50:  # Adjust the number of points for the temporary path
            path.pop(0)
    
        if diff_angle(vector(0, -1, 0), beyblade.axis) > radians(69):  # Correct axis orientation
            print("Top has fallen")
            break
