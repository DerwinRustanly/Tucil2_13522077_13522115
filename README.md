# Tugas Kecil 2 Generator Kurva Bézier

## Table of Contents

- [Tugas Kecil 2 Genarator Kurva Bézier](#tugas-kecil-2-generator-kurva-bézier)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Problem Description](#problem-description)
  - [Program Features](#program-features)
  - [Algorithm Description](#algorithm-description)
  - [Running The Program](#running-the-program)
  - [Libraries Used](#libraries-used)

## Project Description

A Generator Kurva Bézier using the Divide and Conquer Algorithm, Bandung Institute of Technology, made by Enrique Yanuar (13522077) and Derwin Rustanly (13522115) for the Algorithm & Design Course

## Problem Description

The project focuses on generating Bézier curves with \(n\) control points over \(i\) iterations. This process involves utilizing a Divide and Conquer approach to efficiently create the curve, and contrasts this method with a Brute Force Approach for comparison. The aim is to explore how the iterative and recursive nature of the Divide and Conquer strategy can optimize the generation of complex Bézier curves, which are fundamental in computer graphics for modeling smooth curves. By adjusting the number of control points and iterations, the project investigates the nuances of curve generation and the efficiency of different algorithms in handling higher-dimensional Bézier curves.

## Program Features

The features of our program:

- Insert an array of point coordinates.
- Insert the number of iterations to observe the process.
- View an animation of generating the Bezier curve.
- Generate a Bezier curve using the Divide and Conquer algorithm.
- Generate a Bezier curve using the Brute Force algorithm.

## Algorithm Description

### Divide and Conquer Algorithm for Generating Bezier Curves

The Divide and Conquer algorithm is a strategy that divides a problem into smaller, more manageable sub-problems (divide), solves each sub-problem directly if they are small enough (solve), and then combines the solutions of the sub-problems to form a solution for the original problem. For generating Bezier curves, this approach can be implemented using the midpoint algorithm.

#### Implementation of Divide and Conquer for Quadratic Bezier Curves:

1. **Initialization**: Begin with an array containing the first control point. Set the initial iteration count to 0.

2. **Dividing Step**:

   - If the current iteration is less than the desired number of iterations, calculate the midpoint between every two adjacent control points. Specifically, find the midpoint \(M1\) on the line connecting the first control point \(P1\) and the second control point \(P2\), and the midpoint \(M2\) between the second control point \(P2\) and the third control point \(P3\).
   - Next, determine the midpoint \(M3\) between the two midpoints \(M1\) and \(M2\) previously calculated.

3. **Recursive Division**:

   - Recursively repeat steps 2 and 3, increasing the iteration count by 1 each time, to form the left sub-curve. Adjust the control points for the left sub-curve to \(P1\), \(M1\), and \(M3\) until the current iteration equals the desired number of iterations.
   - Add the point \(M3\) to the array initialized in step 1.

4. **Right Sub-curve Formation**:

   - Similarly, recursively repeat steps 2 and 3, increasing the iteration count by 1, to form the right sub-curve. This time, adjust the control points for the right sub-curve to \(M3\), \(M2\), and \(P3\).

5. **Finalization**:
   - Add the final control point \(P3\) to the array initialized in step 1.

The algorithm effectively divides the original Bezier curve into two halves at each iteration, based on their midpoints, resulting in a left and a right Bezier curve. With each iteration, the curve is divided into increasingly simpler sub-curves. As the number of iterations increases, the resulting curve becomes smoother, providing a more detailed approximation of the Bezier curve. This divide and conquer method allows for an efficient and recursive approach to generating Bezier curves, particularly useful in computer graphics and animation for creating smooth and complex shapes.

## Running The Program

To run the program, simply run the `guy.py` python script in the `src` folder

## Libraries Used

To ensure the proper functionality of the program, the following libraries are necessary. Make sure to have them installed in your environment:

- Numpy
- Matplotlib
- ast
- sys
- math
- tkinter
- Time
