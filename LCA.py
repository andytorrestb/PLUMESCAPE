import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class LandingPad:
    """
    Represents a landing pad design with its specific parameters and methods for analysis.
    """
    def __init__(self, name, dust_coeff, erosion_coeff, construction_cost, maintenance_interval):
        self.name = name
        self.dust_coeff = dust_coeff  # kg/m²/kN/m
        self.erosion_coeff = erosion_coeff  # cm/kN
        self.construction_cost = construction_cost  # $
        self.maintenance_interval = maintenance_interval  # months

    def calculate_dust_deposition(self, thrust, distance):
        """
        Calculates dust deposition based on thrust and distance from the pad.
        """
        return self.dust_coeff * thrust / distance**2

    def calculate_erosion(self, thrust):
        """
        Calculates erosion per landing based on thrust.
        """
        return self.erosion_coeff * thrust

    def calculate_maintenance_cost(self, lifetime_months):
        """
        Calculates the total maintenance cost over the lifetime of the pad.
        """
        return self.construction_cost * (lifetime_months / self.maintenance_interval)


class TradeStudy:
    """
    Conducts a trade study on multiple landing pad designs and location combinations.
    """
    def __init__(self, pads, vehicle_thrust, lifetime_months):
        self.pads = pads
        self.vehicle_thrust = vehicle_thrust  # kN
        self.lifetime_months = lifetime_months  # months

    def run_full_study(self, distances, frequencies):
        """
        Runs the trade study for various distances and landing frequencies.
        """
        results = []
        for pad in self.pads:
            for solar_distance in distances:
                for freq in frequencies:
                    # Dust deposition for solar arrays
                    dust_solar = pad.calculate_dust_deposition(self.vehicle_thrust, solar_distance) * freq

                    # Erosion per landing and per month
                    erosion_per_landing = pad.calculate_erosion(self.vehicle_thrust)
                    erosion_per_month = erosion_per_landing * freq

                    # Collect results
                    results.append({
                        'Pad': pad.name,
                        'Solar_Distance (m)': solar_distance,
                        'Frequency (landings/month)': freq,
                        'Dust_Solar (kg/m²/month)': dust_solar,
                        'Erosion (cm/month)': erosion_per_month
                    })
        return results

    def plot_3d_results(self, results):
        """
        Plots the results for all landing pads in a 3D graph.
        """
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_subplot(111, projection='3d')

        for pad in self.pads:
            solar_distances = []
            frequencies = []
            dust_solar = []

            for result in results:
                if result['Pad'] == pad.name:
                    solar_distances.append(result['Solar_Distance (m)'])
                    frequencies.append(result['Frequency (landings/month)'])
                    dust_solar.append(result['Dust_Solar (kg/m²/month)'])

            # Convert to numpy arrays for 3D plotting
            solar_distances = np.array(solar_distances)
            frequencies = np.array(frequencies)
            dust_solar = np.array(dust_solar)

            ax.plot_trisurf(solar_distances, frequencies, dust_solar, label=pad.name, alpha=0.7)

        ax.set_xlabel("Distance to Solar Arrays (m)")
        ax.set_ylabel("Landing Frequency (landings/month)")
        ax.set_zlabel("Dust Deposition (kg/m²/month)")
        ax.set_title("3D Dust Deposition Analysis Across Landing Pads")
        plt.legend()
        plt.savefig('trade_study.png')


if __name__ == "__main__":
    # Define landing pad designs
    pads = [
        LandingPad("Bare Regolith Pad (BRP)", 0.02, 0.1, 500_000, 1),
        LandingPad("Hardened Surface Pad (HSP)", 0.01, 0.05, 2_000_000, 6),
        LandingPad("Bermed Pad (BP)", 0.005, 0.05, 2_500_000, 12),
        LandingPad("Hybrid Multi-Layer Pad (HMP)", 0.003, 0.02, 3_500_000, 18),
    ]

    # Define shared parameters for the trade study
    vehicle_thrust = 40  # kN
    lifetime_months = 120  # 10 years

    # Define range of distances and landing frequencies
    distances = [30, 40, 50, 60, 70]  # m
    frequencies = [5, 10, 15, 20]  # landings/month

    # Run the trade study
    trade_study = TradeStudy(pads, vehicle_thrust, lifetime_months)
    results = trade_study.run_full_study(distances, frequencies)

    # Plot 3D results
    trade_study.plot_3d_results(results)
