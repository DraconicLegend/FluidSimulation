
# Fluid Simulation

## Purpose
This simulation was largely based on [this video](https://www.youtube.com/watch?v=KMfcF9XvVio) by the channel "Machine Learning & Simulation". I wanted to create an animation of a flow field as I thought it would be cool to observe how water acts under certain conditions. I'm posted this on Github so other people can play around with it and become equally fascinated with fluids.

## Directions
Using the plume.py file, there are a few things to note:

### "N_TIME_STEPS" variable
The small this value, the more steps the differential equation will be integrated over. Time steps are inversely proportional to error. That is, the greater the number of steps, the lower the error and vice versa.

### Varying characterisitcs of the inflow
If one desires, they can change the shape, magnitude, and position of the inflow by editing the SoftGeometryMask in lines 33-38 of plume.py in accordance with the [PhiFlow documentation](https://tum-pbs.github.io/PhiFlow/).

### Wind
Vary the values inside the parentheses of the wind variable(line 48) to have a vector field W(x,y) = <x,y> acting on the system throughout the simulation process.
### The Theory Behind the Program - Guided by Machine Learning & Simulation's Explanation

To create a highly accurate fluid simulation, one would use numerical integration techniques or a library that does the needed heavy lifting in the background to solve the incompressible Navier-Stokes equations in conjunction with an advection equation in a closed box.

Momentum:           ∂u/∂t + (u ⋅ ∇) u = − 1/ρ ∇p + ν ∇²u + f

Incompressibility:  ∇ ⋅ u = 0

Advection:          ∂s/∂t + (u ⋅ ∇) s = α ∇²s + i

u:  Velocity (2d vector)
p:  Pressure
f:  Forcing (here due to Buoyancy)
ν:  Kinematic Viscosity
ρ:  Density (here =1.0)
t:  Time
∇:  Nabla operator (defining nonlinear convection, gradient and divergence)
∇²: Laplace Operator
s:  Concentration of a species (here hot smoke)
α:  Diffusivity of the embedded species
i:  Inflow of hot smoke into the domain.

However, it's important to note that plume.py does not account for diffusion. If you want to add diffusion, you can consult the [PhiFlow website](https://tum-pbs.github.io/PhiFlow/).


### Scenario of plume.py


    +----------------------------------------------+
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |                                              |
    |           _                                  |
    |          / \                                 |
    |         |   |                                |
    |          \_/                                 |
    |                                              |
    +----------------------------------------------+

-> Domain is square and closed-off (wall BC everywhere)
-> Initially, the fluid is at rest
-> Initially, the concentration of smoke is zero everywhere
-> There is a continuous inflow of hot smoke in a small circular
   patch in the bottom left of the domain
-> The hot smoke exerts a force on the fluid due to Buyancy
-> This makes the fluid flow upwards and create a plume pattern

-------

Solution strategy:

Initialize the fluid velocity vectors to zero on a Staggered Grid.

Initialize the smoke density to zero on a Centered Grid.

1. Advect the smoke density by a MacCormack step

2. Add the inflow of hot smoke to the smoke density field

3. Compute the Buoyancy force by re-sampling the centered
   smoke densities on the staggered velocities

4. Convect the fluid by means of a semi-lagrangian self-avection
   step 

5. Add the Buoyancy force to the fluid

6. Make the fluid incompressible

7. Repeat

Although diffusion was discluded for simplicity, the involved
convection/advection account for a portion of numerical
diffusion that stabilizes the simulation.
