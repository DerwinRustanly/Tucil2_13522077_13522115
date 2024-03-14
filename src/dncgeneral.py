import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import ast
import time

# Define necessary functions for Bézier curve generation
def sort_coordinates_by_shortest_path(coordinates):
    sorted_coords = [coordinates[0]]
    remaining_coords = set(coordinates[1:])
    
    while remaining_coords:
        last_coord = sorted_coords[-1]
        next_coord = min(remaining_coords, key=lambda x: np.linalg.norm(np.array(last_coord) - np.array(x)))
        sorted_coords.append(next_coord)
        remaining_coords.remove(next_coord)
    
    return sorted_coords

def midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

def divide_and_conquer_bezier(points, all_points, current, iteration, n):
    if current < iteration:
        midPoint = [points.copy()]
        for i in range(n-1):
            subMidPoint = []
            for j in range(n-1-i):
                subMidPoint.append(midpoint(midPoint[i][j], midPoint[i][j+1]))
            midPoint.append(subMidPoint)
        
        for i in range(n-2):
            if points[1] not in all_points:
                all_points.append(points[1])
            points.remove(points[1])
        current += 1
        leftpoints = [midPoint[i][0] for i in range(n)]
        divide_and_conquer_bezier(leftpoints, all_points, current, iteration, n)
        for lp in leftpoints:
            if lp not in points:
                points.append(lp)
            if lp not in all_points:
                all_points.append(lp)
        l = len(leftpoints)
        if leftpoints[l//2] in points:
            points.remove(leftpoints[l//2])
        if l % 2 == 0:
            if leftpoints[l//2-1] in points:
                points.remove(leftpoints[l//2-1])
        
        rightpoints = [midPoint[i][-1] for i in range(n-1, -1, -1)]
        divide_and_conquer_bezier(rightpoints, all_points, current, iteration, n)
        for rp in rightpoints:
            if rp not in points:
                points.append(rp)
            if rp not in all_points:
                all_points.append(rp)
        l = len(rightpoints)
        if rightpoints[l//2] in points:
            points.remove(rightpoints[l//2])
        if l % 2 == 0:
            if rightpoints[l//2-1] in points:
                points.remove(rightpoints[l//2-1])

# Tkinter window setup
window = Tk()
window.title("Bezier Curve Generator")

fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=window)

def generate_bezier(iterations, control_points):
    bezier_points = control_points.copy()
    all_points = control_points.copy()

    divide_and_conquer_bezier(bezier_points, all_points, 0, iterations, len(bezier_points))
    
    bezier_points = sort_coordinates_by_shortest_path(bezier_points)
    bezier_points_np = np.array(bezier_points)

    # Clear the previous plot
    ax.clear()

    # Plot the updated curve
    ax.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
    ax.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Bézier Curve using Divide and Conquer')
    ax.grid(True)

    canvas.draw()

def on_generate_button_clicked():
    iterations = int(iterations_entry.get())
    input_points = str(control_points_entry.get())
    points = ast.literal_eval(input_points)

    start = time.time()
    generate_bezier(iterations, points)
    end = time.time()
    execution_time = (end - start) * 1000  # Calculate execution time in milliseconds

    # Display execution time
    execution_time_label.config(text=f"Execution Time: {execution_time:.2f} ms")

    

label = Label(window, text="Enter number of iterations:")
label.pack()

iterations_entry = Entry(window)
iterations_entry.pack()
label1 = Label(window, text="Enter number of control points:")
label1.pack()
control_points_entry = Entry(window)
control_points_entry.pack()

generate_button = Button(window, text="Generate Curve", command=on_generate_button_clicked)
generate_button.pack()

# Label for displaying the execution time - this is new
execution_time_label = Label(window, text="Execution Time: 0 ms")
execution_time_label.pack() 

canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

window.mainloop()
