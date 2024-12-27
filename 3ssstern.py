import numpy as np
import ternary
import matplotlib.pyplot as plt

def compute_misfit_parameter(alpha, delta_ai_a, delta_i):
    return (alpha * (delta_ai_a ** 2) + delta_i ** 2) ** (2 / 3)

def compute_solid_solution_strength(elements): 
    shear_modulus = sum(element["concentration"] * element["shear_modulus"] for element in elements)

    mu_squared_contributions = 0
    for element in elements:
        ci = element["concentration"]
        delta_ai_a = element["lattice_misfit"]
        delta_i = element["modulus_mismatch"]
        alpha = element["alpha"]

        mu_i = compute_misfit_parameter(alpha, delta_ai_a, delta_i)

        mu_squared_contributions += (mu_i ** 2) * ci

    solid_solution_strength = shear_modulus * (mu_squared_contributions ** (2 / 3)) / 45
    return solid_solution_strength, shear_modulus

def test_mixtures_three_elements(element1, element2, element3):
    step = 0.01
    concentrations = np.arange(0, 1 + step, step)
    results = []

    for c1 in concentrations:
        for c2 in concentrations:
            c3 = 1 - c1 - c2 
            if c3 < 0 or c3 > 1:
                continue

            elements = [
                {"name": element1["name"], "concentration": c1, **element1},
                {"name": element2["name"], "concentration": c2, **element2},
                {"name": element3["name"], "concentration": c3, **element3},
            ]

            solid_solution_strength, shear_modulus = compute_solid_solution_strength(elements)
            results.append({
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "solid_solution_strength": solid_solution_strength,
                "shear_modulus": shear_modulus
            })

    return results

# Define custom tick labels for each axis
custom_ticks = [
    {0.0: "0%", 0.25: "25%", 0.5: "50%", 0.75: "75%", 1.0: "100%"},  # Left axis
    {0.0: "0%", 0.25: "25%", 0.5: "50%", 0.75: "75%", 1.0: "100%"},  # Bottom axis
    {0.0: "0%", 0.25: "25%", 0.5: "50%", 0.75: "75%", 1.0: "100%"}   # Right axis
]

def plot_ternary(results, element1_name, element2_name, element3_name):
    """
    Plot results on a ternary graph with concentration levels on the triangle sides.
    """
    # Extract data for plotting
    points = [(res["c1"], res["c2"], res["c3"]) for res in results]
    values = [res["solid_solution_strength"] for res in results]

    # Normalize the values for coloring
    norm = plt.Normalize(vmin=min(values), vmax=max(values))
    cmap = plt.cm.viridis

    # Set the scale for the ternary plot
    scale = 1.0

    # Create the figure and ternary subplot
    figure, tax = ternary.figure(scale=scale)
    tax.set_title("Solid Solution Strength Ternary Plot", fontsize=16)

    # Add data points with color mapping
    for (point, value) in zip(points, values):
        tax.scatter([point], color=cmap(norm(value)), s=50)

    # Add color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Required for ScalarMappable
    cbar = plt.colorbar(sm, ax=tax.get_axes())
    cbar.set_label("Solid Solution Strength (MPa)", fontsize=12)

    # Configure axis labels and gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=0.1, color="black")
    tax.left_axis_label(f"{element2_name} Concentration (fraction)", fontsize=12, offset=0.14)
    tax.right_axis_label(f"{element1_name} Concentration (fraction)", fontsize=12, offset=0.14)
    tax.bottom_axis_label(f"{element3_name} Concentration (fraction)", fontsize=12, offset=0.14)

    # Display ticks along the triangle's sides
    tax.ticks(axis='lbr', multiple=0.1, linewidth=1, clockwise=True, offset=0.02)

    # Render the plot
    tax.clear_matplotlib_ticks()  # Hide default matplotlib ticks
    tax.get_axes().axis('off')   # Turn off Cartesian axes
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    element_properties = {
        "W": {"shear_modulus": 161, "lattice_misfit": 0.012, "modulus_mismatch": 0.03, "alpha": 9},
        "Mo": {"shear_modulus": 126, "lattice_misfit": 0.015, "modulus_mismatch": 0.025, "alpha": 9},
        "Nb": {"shear_modulus": 38, "lattice_misfit": 0.025, "modulus_mismatch": 0.02, "alpha": 9},
        "Ta": {"shear_modulus": 69, "lattice_misfit": 0.02, "modulus_mismatch": 0.018, "alpha": 9},
        "Ti": {"shear_modulus": 44, "lattice_misfit": 0.03, "modulus_mismatch": 0.04, "alpha": 9},
        "Zr": {"shear_modulus": 33, "lattice_misfit": 0.035, "modulus_mismatch": 0.045, "alpha": 9},
        "Cr": {"shear_modulus": 115, "lattice_misfit": 0.01, "modulus_mismatch": 0.015, "alpha": 9},
        "Fe": {"shear_modulus": 82, "lattice_misfit": 0.014, "modulus_mismatch": 0.02, "alpha": 9},
        "V": {"shear_modulus": 47, "lattice_misfit": 0.022, "modulus_mismatch": 0.03, "alpha": 9},
    }
    print("Available elements:")
    for elem in element_properties.keys():
        print(f"- {elem}")
    element1_name = input("Pick element 1: ").strip()
    element2_name = input("Pick element 2: ").strip()
    element3_name = input("Pick element 3: ").strip()
    if (element1_name not in element_properties 
        or element2_name not in element_properties 
        or element3_name not in element_properties):
        print("Error: One or more selected elements are not available. Please try again.")
    else:
        element1 = {"name": element1_name, **element_properties[element1_name]}
        element2 = {"name": element2_name, **element_properties[element2_name]}
        element3 = {"name": element3_name, **element_properties[element3_name]}
        results = test_mixtures_three_elements(element1, element2, element3)

        max_strength_result = max(results, key=lambda res: res["solid_solution_strength"])
        print(f"Highest Solid Solution Strength: {max_strength_result['solid_solution_strength']:.2f} MPa")
        print(f"Composition: {element1_name}: {max_strength_result['c1']:.2f}, "
              f"{element2_name}: {max_strength_result['c2']:.2f}, "
              f"{element3_name}: {max_strength_result['c3']:.2f}")
        
        plot_ternary(results, element1_name, element2_name, element3_name)
