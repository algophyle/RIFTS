import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class State():
    def __init__(self):
        self.position=np.zeros(3)
        self.velocity=np.zeros(3)
        self.orientation=np.zeros(3)
        self.angular_velocity=np.zeros(3)

class RigidBody():
    def __init__(self):
        self.mass=1000.0
        self.inertia=np.zeros(3)
        self.state=State()

class FliSim():
    def __init__(self):
        self.rb=RigidBody()
        self.acc = np.zeros(3)
        self.g=9.81
        self.history=[]

    def dyncalc(self):

        Fg = np.array([0, 0, -self.rb.mass*self.g])
        Ft = np.array([2000, 0, 0])
        F_total = Fg + Ft   
        self.acc = F_total / self.rb.mass

    def integrator(self,dt):   
        
        state=self.rb.state
        state.velocity += self.acc * dt
        state.position += state.velocity * dt

    def sim(self,t,dt=0.01):
        i=0
        while i<=t:
            self.dyncalc()
            self.integrator(dt)
            i=i+dt
            self.history.append(self.rb.state.position.copy())

    def show(self):
        pass
    def app(self):
        pass

def main():

    t = float(input("Enter the duratrion: "))
    dt = float(input("Enter the step size (dt): "))
    
    f = FliSim()
    f.sim(t, dt)

    positions = np.array(f.history)

    x = positions[:, 0]
    z = positions[:, 2]

    print("Final Position:", positions[-1])

    # --------- STATIC PLOT ---------
    plt.figure()
    plt.plot(x, z)
    plt.xlabel("X (m)")
    plt.ylabel("Z (m)")
    plt.title("Trajectory")
    plt.grid()
    plt.show()

    # --------- ANIMATION ---------
    fig, ax = plt.subplots()

    ax.set_xlim(min(x)-1, max(x)+1)
    ax.set_ylim(min(z)-1, max(z)+1)

    point, = ax.plot([], [], 'ro')
    line, = ax.plot([], [], 'b-')

    def update(frame):
        point.set_data([x[frame]], [z[frame]])
        line.set_data(x[:frame], z[:frame])
        return point, line

    ani = FuncAnimation(fig, update, frames=len(x), interval=20)

    plt.xlabel("X (m)")
    plt.ylabel("Z (m)")
    plt.title("Trajectory Animation")
    plt.grid()

    plt.show()
main()