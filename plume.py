# Import libraries

from phi import flow
import matplotlib.pyplot as plt
from tqdm import tqdm

from pyrecorder.recorder import Recorder
from pyrecorder.writers.video import Video

writer = Video("fire.mp4")

N_TIME_STEPS = 1000

def main():
    velocity = flow.StaggeredGrid(
        values =(0.0,0.0), #Defines values of velocity vectors in grids. B/C we want fluid at rest, we can do (0,0)
        extrapolation=0.0, # This extrapolates around the domain -- a value of 0 Prescribes wall boundry condition
        x=250,
        y = 250,# The x and y values are discreitization points that break up continuts data into boxes
        bounds = flow.Box(x=100,y=100)#This defines the size of the window (100 cm x 100 cm) which are discretized as above

        
    )
    smoke = flow.CenteredGrid(
        values=0.0,#We want the smoke to start with 0 velocity
        extrapolation=flow.extrapolation.BOUNDARY,#Prescribes a Neumann Boundry Condition(LMI)
        x=250,#We want a higher resolution for the smoke, so we discreitze it more
        y=250,
        bounds = flow.Box(x=100,y=100),#Obviously we want this to be equal to the velocity field
    )

    inflow = 0.2* flow.CenteredGrid(
        values = flow.SoftGeometryMask(# Allows us to define geometrical primitives in our domain
            flow.Sphere(
                x=40,
                y=9.5,
                radius = 5,
            )
        ),
        extrapolation = 0.0,
        bounds = smoke.bounds,
        resolution = smoke.resolution,
    )
    def step(velocity_prev,smoke_prev,dt=0.2):
        # 1. Advect the smoke density by a MacCormack step
        smoke_next = flow.advect.mac_cormack(smoke_prev,velocity_prev,dt)+inflow
        buoyancy_force = smoke_next * (0.0,0.1) @ velocity #Causes the buoyancy to go upward with vector <0,0.1>. This will reuqire interpolation and remapping of CenteredGrid onto Staggered Grid, which we do with "@ velocity"
        wind = smoke_next*(0,0)
        velocity_tent = flow.advect.semi_lagrangian(velocity_prev,velocity_prev,dt) + buoyancy_force*dt+wind*dt#Fluid self-advectors, so it resembles Navier-Stokes Advection quite well. Vecolity isn't incompressible(breaks one of the N-S equations), so its called "velocity_tent"
        velocity_next, pressure  =flow.fluid.make_incompressible(velocity_tent)# Makes the fluid incompressible and returns two values ' velocity_next, pressure '
        return velocity_next,smoke_next
        # Can add diffusion methods if needed(LMI) 
    
    plt.style.use("dark_background")
    

    with Recorder(writer) as rec:


        for _ in tqdm(range(N_TIME_STEPS)):
            velocity,smoke = step(velocity,smoke)#Takes a step
            smoke_values_extracted = smoke.values.numpy("y,x")#We need to visualize the field, so we convert PhiFlow values to Numpy
            #Need to provide PhiFlow a way to remap the centered grid into Numpy array. To adhere to MATPLOTLIB convent, we use y,x
            plt.imshow(smoke_values_extracted,origin="lower")
            plt.draw()
            plt. pause(0.01)
            rec.record()
            plt.clf()

if __name__== "__main__":
    main()