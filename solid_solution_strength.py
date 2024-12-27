import math

def compute_misfit_parameter(alpha, delta_ai_a, delta_i):
    """
    Compute the misfit parameter μ_i.
    """
    return (alpha * (delta_ai_a ** 2) + delta_i ** 2) ** (1 / 3)

def compute_solid_solution_strength(elements):
    """
    Compute the solid solution strength for an alloy.
    """
    # Calculate the weighted average shear modulus (G)
    shear_modulus = sum(element["concentration"] * element["shear_modulus"] for element in elements)

    # Calculate μ_i^2 * c_i contributions
    mu_squared_contributions = 0
    for element in elements:
        ci = element["concentration"]
        delta_ai_a = element["lattice_misfit"]
        delta_i = element["modulus_mismatch"]
        alpha = element["alpha"]

        # Calculate μ_i for the element
        mu_i = compute_misfit_parameter(alpha, delta_ai_a, delta_i)

        # Add μ_i^2 * c_i to the sum
        mu_squared_contributions += (mu_i ** 2) * ci

    # Calculate solid solution strength
    solid_solution_strength = shear_modulus * (mu_squared_contributions ** (2 / 3)) / 45
    return solid_solution_strength, shear_modulus

def getelem():
    """
    Collect user inputs for alloy composition.
    Returns a list of element property dictionaries with predefined properties.
    """
    # Predefined element properties
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

    # Display available elements
    print("Available elements:")
    for element in element_properties:
        print(f"- {element}")

    # Collect user input for alloy composition
    elements = []
    num_elements = int(input("Enter the number of elements in the alloy: "))
    for i in range(num_elements):
        element_name = input(f"Enter element {i + 1} (choose from the list above): ")
        if element_name in element_properties:
            concentration = float(input(f"Enter atomic fraction of {element_name} (e.g., 0.25): "))
            # Add the selected element's properties and concentration
            element_data = element_properties[element_name]
            element_data["concentration"] = concentration
            elements.append(element_data)
        else:
            print(f"Invalid element name: {element_name}. Please choose from the list above.")
            return getelem()  # Restart input if invalid

    return elements

# Main execution
if __name__ == "__main__":
    elements = getelem()
    # Ensure the atomic fractions sum to 1
    total_fraction = sum(element["concentration"] for element in elements)
    if  math.isclose(total_fraction, 1.0, rel_tol=1e-3):
        # Calculate solid solution strength and shear modulus
        solid_solution_strength, shear_modulus = compute_solid_solution_strength(elements)
        # Display the results
        print(f"\nWeighted Average Shear Modulus (G): {shear_modulus:.6f} GPa")
        print(f"Solid Solution Strengthening Contribution: {solid_solution_strength:.6f} MPa")
