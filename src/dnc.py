import numpy as np
import matplotlib.pyplot as plt
import time

def midpoint(p1, p2):
    return (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2
def divide_and_conquer_bezier(points, all_points, current, iteration):
    if current < iteration:
        mid1 = midpoint(points[0],points[1])
        mid2 = midpoint(points[1],points[2])
        mid3 = midpoint(mid1, mid2)
        if points[1] not in all_points:
            all_points.append(points[1])
        points.remove(points[1])
        current+=1
        leftpoints = [points[0],mid1,mid3]
        divide_and_conquer_bezier(leftpoints, all_points, current, iteration)
        for lp in leftpoints:
            if lp not in points:
                points.append(lp)
            if lp not in all_points:
                all_points.append(lp)
        if mid1 in points:
            points.remove(mid1)
        rightpoints = [mid3, mid2, points[1]]
        divide_and_conquer_bezier(rightpoints, all_points, current, iteration)
        for rp in rightpoints:
            if rp not in points:
                points.append(rp)
            if rp not in all_points:
                all_points.append(rp)
        if mid2 in points:
            points.remove(mid2)
 


# Control points for a quadratic Bézier curve
control_points = [(0, 0), (1, 2), (2, 0)]
bezier_points = control_points.copy()
all_points = control_points.copy()

# Iterations
iterations = int(input()) # More iterations for a smoother curve

# Generate the curve
start = time.time()
divide_and_conquer_bezier(bezier_points, all_points, 0, iterations)
end = time.time()
print((end-start)*1000)

# Convert to numpy array for plotting
# print(control_points)
bezier_points_np = np.array(bezier_points)
bezier_points_np = bezier_points_np[np.argsort(bezier_points_np[:, 0])]
# print(bezier_points_np)

# Plotting
plt.figure(figsize=(5, 5))
plt.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
plt.plot(np.array(all_points)[:, 0], np.array(all_points)[:, 1], 'go', label='Points')
plt.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Quadratic Bézier Curve using Divide and Conquer')
plt.grid(True)
plt.show()
