# src/scaling.py
import cv2
import numpy as np

def get_scale_factor(frame: np.ndarray, known_ref_size_cm: float) -> float | None:
    """
    Determines the pixel-to-cm conversion factor using a blue reference object.

    Args:
        frame (np.ndarray): The input image frame containing the reference object.
        known_ref_size_cm (float): The known size (e.g., diameter) of the reference object in cm.

    Returns:
        float | None: The calculated scale factor (cm/pixel), or None if not found.
    """
    if frame is None:
        print("Error: Input frame for scaling is None.")
        return None

    print("Finding scale factor using reference object...")
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for a blue color
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for the blue color
    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Warning: No reference object found. Returning default scale factor.")
        return None

    # Assume the largest blue contour is the reference object
    ref_contour = max(contours, key=cv2.contourArea)
    _, _, w, _ = cv2.boundingRect(ref_contour)

    if w == 0:
        print("Warning: Reference object width is zero. Cannot calculate scale.")
        return None

    # Calculate scale factor
    scale_factor = known_ref_size_cm / w
    print(f"Reference object found with pixel width {w}.")
    print(f"Calculated scale factor: {scale_factor:.4f} cm/pixel")

    return scale_factor

def get_manual_scale_factor(manual_scale_cm_per_pixel: float) -> float:
    """
    Returns a manually provided scale factor.

    Args:
        manual_scale_cm_per_pixel (float): The user-defined scale factor in cm/pixel.

    Returns:
        float: The provided scale factor.
    """
    print(f"Using manual scale factor: {manual_scale_cm_per_pixel} cm/pixel")
    return manual_scale_cm_per_pixel
