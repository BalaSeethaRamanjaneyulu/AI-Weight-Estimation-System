# src/geometry.py
import cv2
import numpy as np

def calculate_area(mask: np.ndarray) -> tuple[float, tuple[int, int, int, int] | None]:
    """
    Calculates the 2D area and bounding box from a binary mask.

    Args:
        mask (np.ndarray): The binary mask of the segmented object.

    Returns:
        tuple[float, tuple | None]: A tuple containing:
            - The area of the object in square pixels.
            - The bounding box (x, y, w, h) of the object, or None.
    """
    if mask is None or mask.size == 0:
        print("Error: Input mask for area calculation is invalid.")
        return 0, None

    # Area is the number of non-zero pixels
    area_pixels = np.count_nonzero(mask)

    # Find contours to get the bounding box
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return area_pixels, None

    # Assume the largest contour is the object
    largest_contour = max(contours, key=cv2.contourArea)
    bounding_box = cv2.boundingRect(largest_contour)

    print(f"Calculated area: {area_pixels} pixels^2")
    print(f"Bounding box (x,y,w,h): {bounding_box}")

    return float(area_pixels), bounding_box
