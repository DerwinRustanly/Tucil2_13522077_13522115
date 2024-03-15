import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import ast
import time
import sys

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

def get_midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

def divide_and_conquer_bezier(control_points, bezier_points, current, iteration, n):
    if current < iteration:
        midPoints = []
        midPoints.append(control_points.copy())
        for i in range (n-1):
            subMidPoint = []
            for j in range (n-1-i):
                subMidPoint.append(get_midpoint(midPoints[i][j] ,midPoints[i][j+1]))
            midPoints.append(subMidPoint)
        
        leftpoints = [midPoints[i][0] for i in range(len(midPoints))]
        rightpoints = [midPoints[i][-1] for i in range(len(midPoints)-1,-1,-1)]
        current+=1
        divide_and_conquer_bezier(leftpoints, bezier_points, current, iteration, n)
        bezier_points.append(midPoints[-1][0])
        divide_and_conquer_bezier(rightpoints, bezier_points, current, iteration, n)


# Tkinter window setup
window = Tk()
window.title("Bezier Curve Generator")

fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=window)

def generate_bezier(iterations, control_points):
    bezier_points = [control_points[0]]
    divide_and_conquer_bezier(control_points, bezier_points, 0, iterations, len(control_points))
    bezier_points.append(control_points[-1])
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


def on_closing():
    window.destroy()
    sys.exit()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
