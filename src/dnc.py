import numpy as np
import matplotlib.pyplot as plt
import time

# Function to calculate the midpoint between two points
def get_midpoint(p1, p2):
    return (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2

# Recursive function for generating Bézier points using divide and conquer approach
def divide_and_conquer_bezier(control_points, bezier_points, current, iteration, n):
    if current < iteration:
        # Initialize list to store midpoints for each subdivision
        midPoints = []
        midPoints.append(control_points.copy())
        for i in range (n-1):
            subMidPoint = []
            for j in range (n-1-i):
                subMidPoint.append(get_midpoint(midPoints[i][j] ,midPoints[i][j+1]))
            midPoints.append(subMidPoint)
        # Divide the control points into left and right parts for further subdivision
        leftpoints = [midPoints[i][0] for i in range(len(midPoints))]
        rightpoints = [midPoints[i][-1] for i in range(len(midPoints)-1,-1,-1)]
        current+=1
        divide_and_conquer_bezier(leftpoints, bezier_points, current, iteration, n)
        # Add the midpoint of the last subdivision to the Bézier points
        bezier_points.append(midPoints[-1][0])
        divide_and_conquer_bezier(rightpoints, bezier_points, current, iteration, n)

# Main function to generate and plot the Bézier curve using dnc
def generate_bezier():
    start = time.time()
    iterations = int(input("Enter the number of iterations for smoothness: ")) # More iterations for a smoother curve
    control_points = [(0, 0), (1,8), (5, 0), (8, 10), (14, 0), (20, 15), (25,20), (35,30), (20,4), (10,0)]
    bezier_points = [control_points[0]]
    divide_and_conquer_bezier(control_points, bezier_points, 0, iterations, len(control_points))
    bezier_points.append(control_points[-1])
    end = time.time()
    print(f"Time taken: {(end-start)*1000} ms")
    bezier_points_np = np.array(bezier_points)
    plt.figure(figsize=(5, 5))
    plt.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
    plt.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Quadratic Bézier Curve using Divide and Conquer')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    generate_bezier()