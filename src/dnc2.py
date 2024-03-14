import numpy as np
import matplotlib.pyplot as plt
import time

def midpoint(p1, p2):
    return (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2
def divide_and_conquer_bezier(points, all_points, current, iteration, n):
    if current < iteration:
        rightmost = points[-1]
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
 
        points.remove(rightmost)
        points.append(rightmost)


control_points = [(0, 0), (1,8), (5, 0), (8, 10), (14, 0), (20, 15), (25,20), (35,30), (20,4), (10,0)]
list_iterations = []
iterations = int(input())

start = time.time()
for i in range(iterations):
    bezier_points = control_points.copy()
    all_points = control_points.copy()
    divide_and_conquer_bezier(bezier_points, all_points, 0, i+1, len(bezier_points))
    bezier_points_np = np.array(bezier_points)
    list_iterations.append(bezier_points)
end = time.time()
print((end-start)*1000)

plt.figure(figsize=(10, 10))
plt.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
plt.plot(np.array(all_points)[:, 0], np.array(all_points)[:, 1], 'go', label='Points')
base_color = np.array([0.1, 0.2, 0.5, 0.3])
alpha_step = (1.0 - base_color[3]) / len(list_iterations)

for i in range(len(list_iterations)):
    list_iterations_i_np = np.array(list_iterations[i])
    
    current_color = base_color.copy()
    current_color[3] += i * alpha_step
    
    plt.plot(list_iterations_i_np[:, 0], list_iterations_i_np[:, 1], 'o-', color=current_color, label='Bézier Curve iteration {}'.format(i))


plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Bézier Curve using Divide and Conquer')
plt.grid(True)
plt.show()
