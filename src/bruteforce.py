import numpy as np
import matplotlib.pyplot as plt
import time
from math import comb

# Function to calculate a single point on the Bézier curve
def calculate_bezier_point(t, control_points, n):
    point = np.zeros(2)
    for i, p in enumerate(control_points):
        # Calculate Bernstein basis
        bernstein_coeff = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        point += np.array(p) * bernstein_coeff
    return point

# Function to compute the Bézier curve points using brute force method
def brute_force_bezier(control_points, iterations):
    n = len(control_points) - 1
    bezier_points = []
    num_points = 2**iterations+1
    for t in np.linspace(0, 1, num_points):
        bezier_points.append(calculate_bezier_point(t, control_points, n))
    return bezier_points

# Main function to generate and plot the Bézier curve using brute force
def generate_bezier_brute_force():
    start = time.time()
    iterations = int(input("Enter the number of iterations for smoothness: ")) # More iterations for a smoother curve
    control_points = [(0, 0), (1,8), (5, 0), (8, 10), (14, 0), (20, 15), (25,20), (35,30), (20,4), (10,0)]
    
    bezier_points = brute_force_bezier(control_points, iterations)
    
    end = time.time()
    print(f"Time taken: {(end-start)*1000} ms")
    
    bezier_points_np = np.array(bezier_points)
    plt.figure(figsize=(5, 5))
    plt.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
    plt.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Quadratic Bézier Curve using Brute Force')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    generate_bezier_brute_force()
