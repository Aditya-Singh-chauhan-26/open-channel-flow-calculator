import streamlit as st

def main():
    # Page Header
    st.title("🌊 Open Channel Flow Calculator")
    st.write("Calculate velocity and discharge using Chezy's and Manning's equations.")

    # Sidebar: Geometry Inputs
    st.sidebar.header("1. Channel Geometry")
    shape = st.sidebar.selectbox("Channel Shape", ["Rectangular", "Trapezoidal"])
    b = st.sidebar.number_input("Bottom Width (m)", min_value=0.1, value=2.0)
    y = st.sidebar.number_input("Flow Depth (m)", min_value=0.1, value=1.5)
    
    if shape == "Trapezoidal":
        z = st.sidebar.number_input("Side Slope (H:V)", min_value=0.0, value=1.0)
    else:
        z = 0.0

    # Sidebar: Flow Parameters
    st.sidebar.header("2. Flow Parameters")
    S = st.sidebar.number_input("Bed Slope (m/m)", min_value=0.0001, value=0.001, format="%.4f")
    equation = st.sidebar.radio("Calculation Method", ["Manning's Equation", "Chezy's Equation"])

    if equation == "Manning's Equation":
        coef = st.sidebar.number_input("Manning's n (Roughness)", min_value=0.005, value=0.013, format="%.3f")
    else:
        coef = st.sidebar.number_input("Chezy's C (Resistance)", min_value=10.0, value=50.0)

    # Mathematical Engine
    if shape == "Rectangular":
        A = b * y
        P = b + 2 * y
    else: # Trapezoidal
        A = y * (b + z * y)
        P = b + 2 * y * ((1 + z**2)**0.5)

    R = A / P

    if equation == "Manning's Equation":
        v = (1 / coef) * (R**(2/3)) * (S**0.5)
    else:
        v = coef * ((R * S)**0.5)

    Q = A * v

    # Main Page: Display Results
    st.header("Calculation Results")
    
    # Displaying metrics in columns for a clean dashboard look
    col1, col2 = st.columns(2)
    col1.metric("Cross-sectional Area (A)", f"{A:.3f} m²")
    col1.metric("Wetted Perimeter (P)", f"{P:.3f} m")
    col1.metric("Hydraulic Radius (R)", f"{R:.3f} m")
    
    col2.metric("Average Velocity (v)", f"{v:.3f} m/s")
    col2.metric("Total Discharge (Q)", f"{Q:.3f} m³/s")

if __name__ == "__main__":
    main()