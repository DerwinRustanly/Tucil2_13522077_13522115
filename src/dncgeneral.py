import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
def sort_coordinates_by_shortest_path(coordinates):
    """
    Sorts a list of coordinates based on the shortest path that connects them,
    starting from the first coordinate.
    
    Args:
    - coordinates (list of tuples): The coordinates to be sorted.
    
    Returns:
    - List of tuples representing the sorted coordinates.
    """
    sorted_coords = [coordinates[0]]  # Start with the first coordinate
    remaining_coords = set(coordinates[1:])  # Remaining coordinates to sort
    
    while remaining_coords:
        last_coord = sorted_coords[-1]
        # Find the closest coordinate to the last one in the sorted list
        next_coord = min(remaining_coords, key=lambda x: np.linalg.norm(np.array(last_coord) - np.array(x)))
        sorted_coords.append(next_coord)
        remaining_coords.remove(next_coord)
    
    return sorted_coords

# # Given array of coordinates
# arr = [(0,0), (0,1), (3,3), (2,2)]

# # Sort the array based on the shortest path
# sorted_arr = sort_coordinates_by_shortest_path(arr)
# sorted_arr

def midpoint(p1, p2):
    return (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2
def divide_and_conquer_bezier(points, all_points, current, iteration, n):
    if current < iteration:
        midPoint =[]
        midPoint.append(points.copy())
        for i in range (n-1):
            subMidPoint = []
            for j in range (n-1-i):
                subMidPoint.append(midpoint(midPoint[i][j] ,midPoint[i][j+1]))
            midPoint.append(subMidPoint)
        
        for i in range (n-2):
            if points[1] not in all_points:
                all_points.append(points[1])
            points.remove(points[1])
        current+=1
        leftpoints = []
        for i in range (n):
            leftpoints.append(midPoint[i][0])
        divide_and_conquer_bezier(leftpoints, all_points, current, iteration, n)
        for lp in leftpoints:
            if lp not in points:
                points.append(lp)
            if lp not in all_points:
                all_points.append(lp)
        l = len(leftpoints)
        if leftpoints[l//2] in points:
            points.remove(leftpoints[l//2])
        if l%2==0:
            if leftpoints[l//2-1] in points:
                points.remove(leftpoints[l//2-1])
        
        rightpoints = []
        for i in range (n-1, -1, -1):
            rightpoints.append(midPoint[i][-1])
        divide_and_conquer_bezier(rightpoints, all_points, current, iteration, n)
        for rp in rightpoints:
            if rp not in points:
                points.append(rp)
            if rp not in all_points:
                all_points.append(rp)
        l = len(rightpoints)
        if rightpoints[l//2] in points:
            points.remove(rightpoints[l//2])
        if l%2==0:
            if rightpoints[l//2-1] in points:
                points.remove(rightpoints[l//2-1])
 


# Control points for a quadratic Bézier curve
control_points = [(0, 0), (1,8), (5, 0), (8, 10), (14, 0), (20, 15), (25,20), (35,30), (20,4), (10,0)]
bezier_points = control_points.copy()
all_points = control_points.copy()

# Iterations
iterations = int(input()) # More iterations for a smoother curve

# Generate the curve
start = time.time()
# print(len(bezier_points))
divide_and_conquer_bezier(bezier_points, all_points, 0, iterations, len(bezier_points))
end = time.time()
print((end-start)*1000)

# Convert to numpy array for plotting
bezier_points = sort_coordinates_by_shortest_path(bezier_points)
bezier_points_np = np.array(bezier_points)

# Prepare the initial plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
ax.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
points_plot, = ax.plot([], [], 'go', label='Points')  # Placeholder for green points
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Bézier Curve using Divide and Conquer')
ax.grid(True)

# Update function for the animation
def update(frame):
    points_plot.set_data(np.array(all_points[:frame+1])[:, 0], np.array(all_points[:frame+1])[:, 1])
    return points_plot,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(all_points), blit=True, interval=100)

plt.show()