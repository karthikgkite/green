import streamlit as st

import sympy as sp

import numpy as np

import matplotlib.pyplot as plt

from scipy.integrate import dblquad

from sympy import lambdify



# Define the main function

def green_theorem_calculator():

    # Streamlit UI

    st.title("Green's Theorem Calculator")

    

    # Step 1: Input for P(x, y) and Q(x, y)

    st.header("Enter the functions P(x, y) and Q(x, y):")

    P_input = st.text_input("Enter P(x, y):", "x*2 + y*2")

    Q_input = st.text_input("Enter Q(x, y):", "x*y + y**2")

    

    # Convert input strings to sympy expressions

    x, y = sp.symbols('x y')

    P = sp.sympify(P_input)

    Q = sp.sympify(Q_input)

    

    # Step 2: Compute the partial derivatives

    dQ_dx = sp.diff(Q, x)

    dP_dy = sp.diff(P, y)

    

    # Display partial derivatives

    st.write(f"∂Q/∂x = {dQ_dx}")

    st.write(f"∂P/∂y = {dP_dy}")

    

    # Step 3: Set up the region for integration (can be defined here or user-defined)

    st.header("Define the limits for integration:")

    

    x_min = st.number_input("x_min:", value=0)

    x_max = st.number_input("x_max:", value=1)

    y_min = st.number_input("y_min:", value=0)

    y_max = st.number_input("y_max:", value=1)

    

    # Step 4: Convert symbolic expressions to numeric functions using lambdify

    func_dQ_dx = lambdify((x, y), dQ_dx, 'numpy')

    func_dP_dy = lambdify((x, y), dP_dy, 'numpy')

    

    # Define the function to integrate

    def func_to_integrate(x_val, y_val):

        return func_dQ_dx(x_val, y_val) - func_dP_dy(x_val, y_val)

    

    # Step 5: Add a Calculate button

    if st.button("Calculate"):

        # Perform the numerical double integral

        result, error = dblquad(func_to_integrate, x_min, x_max, lambda x: y_min, lambda x: y_max)

        

        # Step 6: Display the result of the integral

        st.header("Result:")

        st.write(f"The value of the double integral is: {result}")

        st.write(f"Numerical integration error estimate: {error}")

        

        # Step 7: Plot the graph of the integrand

        X = np.linspace(x_min, x_max, 100)

        Y = np.linspace(y_min, y_max, 100)

        X, Y = np.meshgrid(X, Y)

        Z = func_to_integrate(X, Y)

        

        # Create a contour plot

        fig, ax = plt.subplots()

        cp = ax.contourf(X, Y, Z, levels=50, cmap='viridis')

        fig.colorbar(cp)

        

        ax.set_title("Contour plot of the integrand")

        ax.set_xlabel('x')

        ax.set_ylabel('y')

        

        st.pyplot(fig)



# Run the Streamlit app

if _name_ == "_main_":

    green_theorem_calculator()
