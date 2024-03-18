import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from tkinter import *
import ast
import time
import sys
from math import comb

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
window.geometry("1200x800")  # Set initial size of the window

# Define a color scheme
bg_color = "#333333"  # Dark grey
text_color = "#FFFFFF"  # White
button_color = "#555555"  # Lighter grey
entry_bg_color = "#474747"  # Entry background
entry_fg_color = "#FFFFFF"  # Entry text color

window.config(bg=bg_color)

# Adjust figure to fit the new UI theme
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().config(bg=bg_color)

def generate_bezier_dnc(iterations, control_points):
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

def calculate_bezier_point(t, control_points, n):
    point = np.zeros(2)
    for i, p in enumerate(control_points):
        # Calculate Bernstein basis
        bernstein_coeff = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        point += np.array(p) * bernstein_coeff
    return point

def generate_bezier_brute_force(iterations, control_points):
    
    n = len(control_points) - 1
    bezier_points = []
    num_points = 2**iterations+1
    for t in np.linspace(0, 1, num_points):
        bezier_points.append(calculate_bezier_point(t, control_points, n))
    bezier_points_np = np.array(bezier_points)

    # Clear the previous plot
    ax.clear()

    # Plot the updated curve
    ax.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')
    ax.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Bézier Curve using Brute Force')
    ax.grid(True)

    canvas.draw()


def on_generate_button_clicked(method):
    try:
        execution_time_label.config(text="On progress dude..", font=("Nirmala UI", 16))
        iterations = int(iterations_entry.get())
        if iterations <= 0:
            raise ValueError("Number of iterations must be greater than 0.")
        input_points = str(control_points_entry.get())
        points = ast.literal_eval(input_points)
        
        # Validate the points format
        if not all(isinstance(point, tuple) and len(point) == 2 for point in points):
            raise ValueError("Control points must be a list of tuples (x, y).")

        start = time.time()
        if method == "divide_and_conquer":
            generate_bezier_dnc(iterations, points)
        elif method == "brute_force":
            generate_bezier_brute_force(iterations, points)
        end = time.time()
        execution_time = (end - start) * 1000  # Calculate execution time in milliseconds

        # Display execution time
        execution_time_label.config(text=f"Execution Time: {execution_time:.2f} ms", font=("Nirmala UI", 16))
    except ValueError as e:
        # Display the error message
        execution_time_label.config(text=f"Error: {str(e)}")
    except SyntaxError:
        # Handle incorrect syntax in control points entry
        execution_time_label.config(text="Error: Invalid syntax in control points.")
    except Exception as e:
        # General error handling
        execution_time_label.config(text=f"Unexpected error: {str(e)}")

# Define necessary functions for animation
def animate_bezier(iterations, control_points):
    def update(frame):
        ax.clear()
        start = time.time()
        ax.plot(np.array(control_points)[:, 0], np.array(control_points)[:, 1], 'ro-', label='Control Points')

        bezier_points = [control_points[0]]
        divide_and_conquer_bezier(control_points, bezier_points, 0, frame + 1, len(control_points))
        bezier_points.append(control_points[-1])
        bezier_points_np = np.array(bezier_points)
        end = time.time()
        execution_time = (end - start) * 1000  # Calculate execution time in milliseconds

        # Display execution time
        execution_time_label.config(text=f"Execution Time: {execution_time:.2f} ms", font=("Nirmala UI", 16))
        ax.plot(bezier_points_np[:, 0], bezier_points_np[:, 1], 'bo-', label='Bézier Curve')
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Bézier Curve Animation - Iteration {}'.format(frame + 1))
        ax.grid(True)

    anim = FuncAnimation(fig, update, frames=iterations, repeat=False)
    canvas.draw()

# Define event handler for the "Generate Animation" button
def on_generate_animation_button_clicked():
    try:
        iterations = int(iterations_entry.get())
        if iterations <= 0:
            raise ValueError("Number of iterations must be greater than 0.")
        input_points = str(control_points_entry.get())
        points = ast.literal_eval(input_points)
        
        # Validate the points format
        if not all(isinstance(point, tuple) and len(point) == 2 for point in points):
            raise ValueError("Control points must be a list of tuples (x, y).")
        
        animate_bezier(iterations, points)

    except ValueError as e:
        # Display the error message
        execution_time_label.config(text=f"Error: {str(e)}")
    except SyntaxError:
        # Handle incorrect syntax in control points entry
        execution_time_label.config(text="Error: Invalid syntax in control points.")
    except Exception as e:
        # General error handling
        execution_time_label.config(text=f"Unexpected error: {str(e)}")

# UI Components setup with updated colors and styles
title = Label(window, text="Bezier Curve Generator", font=("Nirmala UI", 36, "bold"), pady=10, bg=bg_color, fg=text_color)
title.pack()

input_frame = Frame(window, bg=bg_color)
input_frame.pack(pady=20)

label_iterations = Label(input_frame, text="Enter number of iterations:", font=("Nirmala UI", 16), bg=bg_color, fg=text_color)
label_iterations.grid(row=0, column=0, padx=10, sticky="w")
iterations_entry = Entry(input_frame, font=("Nirmala UI", 16), bg=entry_bg_color, fg=entry_fg_color, insertbackground=text_color)  # insertbackground changes cursor color
iterations_entry.grid(row=0, column=1, padx=10, sticky = "ew")

label_points = Label(input_frame, text="Enter control points as list:", font=("Nirmala UI", 16), bg=bg_color, fg=text_color)
label_points.grid(row=1, column=0, padx=10, sticky="w")
control_points_entry = Entry(input_frame, font=("Nirmala UI", 16), width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=text_color)
control_points_entry.grid(row=1, column=1, padx=10)

buttons_frame = Frame(window, bg=bg_color)
buttons_frame.pack(pady=10)
generate_button = Button(buttons_frame, text="Generate Curve (D&C)", font=("Nirmala UI", 16), command=lambda: on_generate_button_clicked(method='divide_and_conquer'), bg=button_color, fg=text_color)
generate_button.grid(row=0, column=0, padx=10)
brute_force_button = Button(buttons_frame, text="Generate Curve (Brute Force)", font=("Nirmala UI", 16), command=lambda: on_generate_button_clicked(method='brute_force'), bg=button_color, fg=text_color)
brute_force_button.grid(row=0, column=1, padx=10)

generate_animation_button = Button(buttons_frame, text="Generate Animation", font=("Nirmala UI", 16), command=on_generate_animation_button_clicked, bg=button_color, fg=text_color)
generate_animation_button.grid(row=0, column=2, padx=10)

execution_time_label = Label(window, text="Execution Time: 0 ms", font=("Nirmala UI", 16), bg=bg_color, fg=text_color)
execution_time_label.pack(pady=10)

canvas.get_tk_widget().pack(fill=BOTH, expand=1, padx=100, pady=20)  # Make the canvas expandable



def on_closing():
    window.destroy()
    sys.exit()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
