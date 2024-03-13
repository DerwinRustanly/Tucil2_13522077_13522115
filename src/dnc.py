import numpy as np
import matplotlib.pyplot as plt
import time

def midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

def divide_and_conquer_bezier(points, all_points, current, iteration):
    if current < iteration:
        # Calculate midpoints for the cubic bezier curve
        mid1 = midpoint(points[0], points[1])
        mid2 = midpoint(points[1], points[2])
        mid3 = midpoint(points[2], points[3])
        mid4 = midpoint(mid1, mid2)
        mid5 = midpoint(mid2, mid3)
        mid6 = midpoint(mid4, mid5)
        
        # Append intermediate points to all_points
        for point in [points[1], points[2], mid1, mid2, mid3, mid4, mid5, mid6]:
            if point not in all_points:
                all_points.append(point)
        
        # Update points and recurse
        left_points = [points[0], mid1, mid4, mid6]
        right_points = [mid6, mid5, mid3, points[3]]
        
        current += 1
        divide_and_conquer_bezier(left_points, all_points, current, iteration)
        divide_and_conquer_bezier(right_points, all_points, current, iteration)

# Control points for a cubic Bézier curve
control_points = [(0, 0), (1, 2), (3, 0), (4, 5)]
bezier_points = control_points.copy()
all_points = control_points.copy()

# Iterations
iterations = int(input("Enter the number of iterations for a smoother curve: "))  # More iterations for a smoother curve

# Generate the curve
start = time.time()
divide_and_conquer_bezier(bezier_points, all_points, 0, iterations)
end = time.time()
print("Execution time:", (end - start) * 1000, "ms")

# Convert to numpy array for plotting
all_points_np = np.array(all_points)
all_points_np = all_points_np[np.argsort(all_points_np[:, 0])]

# Plotting
plt.figure(figsize=(5, 5))
plt.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
plt.plot(all_points_np[:, 0], all_points_np[:, 1], 'bo-', label='Bézier Curve')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Cubic Bézier Curve using Divide and Conquer')
plt.grid(True)
plt.show()
