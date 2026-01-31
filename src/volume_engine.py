# src/volume_engine.py
import numpy as np

def calculate_volume(mask: np.ndarray, scale_factor: float) -> float:
    """
    Estimates the volume of an object from its binary mask using the disk method.
    Assumes the object's major axis is horizontal.

    Args:
        mask (np.ndarray): The binary mask of the segmented object.
        scale_factor (float): The conversion factor from pixels to cm.

    Returns:
        float: The estimated volume of the object in cubic centimeters.
    """
    if mask is None or mask.size == 0 or scale_factor <= 0:
        print("Error: Invalid input for volume calculation.")
        return 0.0

    print("Estimating volume using the Disk Method...")
    total_volume_cm3 = 0.0

    # The thickness of each slice in cm
    slice_thickness_cm = 1.0 * scale_factor

    # Iterate through each row (slice) of the mask
    for row in mask:
        # Find the width of the object in the current slice
        pixel_width = np.count_nonzero(row)

        if pixel_width > 0:
            # Convert width to cm
            width_cm = pixel_width * scale_factor

            # Calculate radius and area of the disk
            radius_cm = width_cm / 2
            disk_area_cm2 = np.pi * (radius_cm ** 2)

            # Volume of the cylindrical disk
            disk_volume_cm3 = disk_area_cm2 * slice_thickness_cm

            # Add to total volume
            total_volume_cm3 += disk_volume_cm3

    print(f"Estimated volume: {total_volume_cm3:.2f} cm^3")
    return total_volume_cm3
