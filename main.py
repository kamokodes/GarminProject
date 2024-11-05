import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants

g = 9.81  # Gravitational acceleration(m/s^2)
goal_x = 28.65
goal_radius = 0.45

# Extract data from csv file

data = pd.read_csv("basketball.csv")


#function to estimate the velocity and goal landing
def predict_goal(sensor_1, sensor_2, dt=0.1):
    dx = sensor_1.diff().dropna()  #change in horizontal distances
    dy = sensor_2.diff().dropna()  #change in vertical distances

    #Estimate initial velocity components using first change

    v_x = dx.iloc[0] / dt
    v_y = dy.iloc[0] / dt

    #Calculate initial speed and launch angle
    v_0 = np.sqrt(v_x ** 2 + v_y ** 2)
    theta = np.arctan2(v_y, v_x)

    #Calculate time of flight
    time_of_flight = (2 * v_y) / g

    #Calculate landing position
    x_landing = v_x * time_of_flight

    #Check if landing position is within goal range
    in_goal = (goal_x - goal_radius) <= x_landing <= (goal_x + goal_radius)

    #Return whether the shot lands in the goal and result
    return in_goal, x_landing, time_of_flight

#Analyze each ball's trajectory
results = {}
for i in range(1,7): #Assuming we have 6 balls
    sensor_1 = data[f'b{i}_s1']
    sensor_2 = data[f'b{i}_s2']

    #predict goal landing
    in_goal, x_landing, time_of_flight = predict_goal(sensor_1, sensor_2)

    # Store result
    results[f'Ball{i}'] = {
        "In Goal": in_goal,
        "Landing Position(x)":x_landing,
        "Time of Flight": time_of_flight
    }

#Output predictions
for ball, result in results.items():
    print(f"{ball} - In Goal:{result['In Goal']}, Landing Position(x):{result['Landing Position(x)']:.2f}meters, Time of Flight:{result['Time of Flight']:.2f} seconds ")

#Trajectories plotted
plt.figure(figsize=(10, 6))
for i in range(1,7):
    sensor_1 = data[f'b{i}_s1']
    time = np.arange(len(sensor_1)) * 0.1

    #Plot distance from sensor 1 over time
    plt.plot(time,sensor_1, label = f'Ball{i}')

plt.xlabel("Time(s)")
plt.ylabel("Distance from Sensor 1 (m)")
plt.title("Distance from sensor 1 over time for each ball")
plt.legend()
plt.show()
