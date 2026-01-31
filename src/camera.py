# src/camera.py
import cv2
import numpy as np

def capture_frame(device_index=0) -> np.ndarray | None:
    """
    Captures a single frame from a specified camera device.

    Args:
        device_index (int): The index of the camera device to use.

    Returns:
        np.ndarray | None: The captured frame as a NumPy array, or None if an error occurred.
    """
    print(f"Attempting to capture frame from camera device {device_index}...")
    cap = cv2.VideoCapture(device_index)

    if not cap.isOpened():
        print(f"Error: Could not open camera device {device_index}.")
        return None

    # Capture a single frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    if not ret:
        print("Error: Failed to capture frame.")
        return None

    # Save the captured frame for debugging and records
    save_path = "data/captured_frame.jpg"
    cv2.imwrite(save_path, frame)
    print(f"Frame captured successfully and saved to {save_path}")

    return frame
