import math
import numpy as np

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

def test_mixtures(element1, element2):
    """
    Test all possible concentrations between two elements.
    """
    concentrations = np.linspace(0, 1, 101)  # Generate 0%, 1%, ..., 100% for each element
    results = []

    for c1 in concentrations:
        c2 = 1 - c1  # Complementary concentration
        elements = [
            {"name": element1["name"], "concentration": c1, **element1},
            {"name": element2["name"], "concentration": c2, **element2}
        ]

        solid_solution_strength, shear_modulus = compute_solid_solution_strength(elements)
        results.append({
            "c1": c1,
            "c2": c2,
            "solid_solution_strength": solid_solution_strength,
            "shear_modulus": shear_modulus
        })

    return results

# Main execution
if __name__ == "__main__":
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

    # Select elements for testing
    print("Available elements:")
    for elem in element_properties.keys():
        print(f"- {elem}")
    
    element1_name = input("Pick element 1: ").strip()
    element2_name = input("Pick element 2: ").strip()

    if element1_name not in element_properties or element2_name not in element_properties:
        print("Error: One or both selected elements are not available. Please try again.")
    else:
        # Retrieve element properties
        element1 = {"name": element1_name, **element_properties[element1_name]}
        element2 = {"name": element2_name, **element_properties[element2_name]}

        # Test all mixtures
        results = test_mixtures(element1, element2)

        # Display the results
        print(f"\nConcentration of {element1_name} (%) | Concentration of {element2_name} (%) | Shear Modulus (G) | Solid Solution Strength (MPa)")
        print("-" * 80)
        for result in results:
            print(f"{result['c1']*100:>21.1f} | {result['c2']*100:>21.1f} | {result['shear_modulus']:.6f} | {result['solid_solution_strength']:.6f}")
