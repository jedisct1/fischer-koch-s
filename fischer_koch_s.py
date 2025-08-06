#!/usr/bin/env python3
"""
Fischer-Koch S Surface Plotter

This program visualizes the Fischer-Koch S triply periodic minimal surface (TPMS)
using the approximated implicit equation:
cos(2x)·sin(y)·cos(z) + cos(2y)·sin(z)·cos(x) + cos(2z)·sin(x)·cos(y) = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import ndimage
from skimage import measure
import warnings

warnings.filterwarnings("ignore")


def fischer_koch_s(x, y, z):
    """
    Evaluate the Fischer-Koch S implicit equation at given points.

    The equation is:
    cos(2x)·sin(y)·cos(z) + cos(2y)·sin(z)·cos(x) + cos(2z)·sin(x)·cos(y) = 0

    Parameters:
    -----------
    x, y, z : numpy arrays
        Coordinates at which to evaluate the function

    Returns:
    --------
    numpy array : Function values at the given points
    """
    return (
        np.cos(2 * x) * np.sin(y) * np.cos(z)
        + np.cos(2 * y) * np.sin(z) * np.cos(x)
        + np.cos(2 * z) * np.sin(x) * np.cos(y)
    )


def generate_surface(resolution=50, bounds=(-np.pi, np.pi), iso_value=0.0):
    """
    Generate the Fischer-Koch S surface using marching cubes algorithm.

    Parameters:
    -----------
    resolution : int
        Number of points along each axis (higher = better quality but slower)
    bounds : tuple
        (min, max) bounds for the coordinate space
    iso_value : float
        Isosurface value (typically 0 for implicit surfaces)

    Returns:
    --------
    verts, faces : arrays
        Vertices and faces of the triangulated surface
    """
    print(f"Generating grid with resolution {resolution}x{resolution}x{resolution}...")

    # Create a 3D grid
    x = np.linspace(bounds[0], bounds[1], resolution)
    y = np.linspace(bounds[0], bounds[1], resolution)
    z = np.linspace(bounds[0], bounds[1], resolution)

    # Create meshgrid
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    # Evaluate the implicit function
    print("Evaluating Fischer-Koch S equation...")
    values = fischer_koch_s(X, Y, Z)

    # Apply Gaussian smoothing for better surface quality
    values = ndimage.gaussian_filter(values, sigma=0.5)

    # Extract the isosurface using marching cubes
    print("Extracting isosurface using marching cubes...")
    verts, faces, normals, values = measure.marching_cubes(
        values, level=iso_value, spacing=(x[1] - x[0], y[1] - y[0], z[1] - z[0])
    )

    # Adjust vertices to correct coordinate system
    verts[:, 0] += bounds[0]
    verts[:, 1] += bounds[0]
    verts[:, 2] += bounds[0]

    return verts, faces


def plot_surface(verts, faces, title="Fischer-Koch S Surface"):
    """
    Plot the 3D surface using matplotlib.

    Parameters:
    -----------
    verts : array
        Vertices of the surface
    faces : array
        Face indices
    title : str
        Title for the plot
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Create the mesh
    ax.plot_trisurf(
        verts[:, 0],
        verts[:, 1],
        verts[:, 2],
        triangles=faces,
        cmap="viridis",
        alpha=0.8,
        edgecolor="none",
        shade=True,
    )

    # Set labels and title
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_zlabel("Z", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")

    # Set equal aspect ratio
    max_range = (
        np.array(
            [
                verts[:, 0].max() - verts[:, 0].min(),
                verts[:, 1].max() - verts[:, 1].min(),
                verts[:, 2].max() - verts[:, 2].min(),
            ]
        ).max()
        / 2.0
    )

    mid_x = (verts[:, 0].max() + verts[:, 0].min()) * 0.5
    mid_y = (verts[:, 1].max() + verts[:, 1].min()) * 0.5
    mid_z = (verts[:, 2].max() + verts[:, 2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Add grid
    ax.grid(True, alpha=0.3)

    # Set viewing angle
    ax.view_init(elev=30, azim=45)

    return fig, ax


def main():
    """Main function to generate and display the Fischer-Koch S surface."""
    print("=" * 60)
    print("Fischer-Koch S Surface Visualization")
    print("=" * 60)
    print("\nThis program generates a 3D visualization of the Fischer-Koch S")
    print("triply periodic minimal surface (TPMS) using the implicit equation:")
    print("cos(2x)·sin(y)·cos(z) + cos(2y)·sin(z)·cos(x) + cos(2z)·sin(x)·cos(y) = 0")
    print("-" * 60)

    # User input for resolution
    try:
        resolution = input("\nEnter grid resolution (30-100, default=50): ").strip()
        resolution = int(resolution) if resolution else 50
        resolution = max(30, min(100, resolution))  # Clamp between 30 and 100
    except ValueError:
        resolution = 50
        print("Using default resolution: 50")

    print(f"\nUsing resolution: {resolution}")
    print("-" * 60)

    # Generate the surface
    try:
        verts, faces = generate_surface(
            resolution=resolution, bounds=(-np.pi, np.pi), iso_value=0.0
        )

        print(f"\nSurface generated successfully!")
        print(f"Vertices: {len(verts)}")
        print(f"Faces: {len(faces)}")

        # Plot the surface
        print("\nRendering 3D visualization...")
        fig, ax = plot_surface(verts, faces)

        # Add interactivity instructions
        print("\n" + "=" * 60)
        print("VISUALIZATION CONTROLS:")
        print("-" * 60)
        print("• Click and drag to rotate the view")
        print("• Right-click and drag to zoom")
        print("• Middle-click and drag to pan")
        print("• Close the window to exit")
        print("=" * 60)

        plt.show()

    except Exception as e:
        print(f"\nError generating surface: {e}")
        print("Please check that all dependencies are installed correctly.")
        return 1

    print("\nVisualization complete!")
    return 0


if __name__ == "__main__":
    exit(main())
