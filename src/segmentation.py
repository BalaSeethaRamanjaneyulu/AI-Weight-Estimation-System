# src/segmentation.py
import cv2
import numpy as np

# Global variables for mouse callback
drawing = False
ix, iy = -1, -1
rect = (0, 0, 0, 0)

def draw_rectangle(event, x, y, flags, param):
    """Mouse callback function to draw a rectangle."""
    global ix, iy, drawing, rect
    frame = param['frame']

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = frame.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Select ROI', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix, iy), (x, y), (0, 255, 0), 2)
        rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))

def segment_object_interactive(frame: np.ndarray) -> np.ndarray | None:
    """
    Performs interactive segmentation using OpenCV's GrabCut algorithm.
    A window will open allowing the user to draw a bounding box around the object.

    Args:
        frame (np.ndarray): The input image frame.

    Returns:
        np.ndarray | None: The binary mask of the segmented object, or None if input is invalid.
    """
    global rect
    if frame is None:
        print("Error: Input frame for segmentation is None.")
        return None

    print("--- Interactive Segmentation ---")
    print("1. Draw a rectangle around the object to segment.")
    print("2. Press 'n' to accept the rectangle and run GrabCut.")
    print("3. Press 'r' to reset.")
    print("4. Press 'q' to quit.")
    print("--------------------------------")

    window_name = "Select ROI"
    cv2.namedWindow(window_name)
    param = {'frame': frame.copy()}
    cv2.setMouseCallback(window_name, draw_rectangle, param)

    while True:
        cv2.imshow(window_name, param['frame'])
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'): # Reset
            param['frame'] = frame.copy()
            rect = (0, 0, 0, 0)
        elif key == ord('n'): # Run GrabCut
            if rect[2] > 0 and rect[3] > 0:
                break
            else:
                print("Please select a valid ROI first.")
        elif key == ord('q'): # Quit
            cv2.destroyAllWindows()
            return None

    cv2.destroyAllWindows()

    print("Running GrabCut algorithm...")
    mask = np.zeros(frame.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    try:
        cv2.grabCut(frame, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    except Exception as e:
        print(f"Error during GrabCut: {e}")
        return None

    # The mask is now 0s and 2s (probable background/foreground) and 1s and 3s (definite background/foreground)
    # We create a binary mask where definite and probable foreground are 1, and the rest are 0.
    binary_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Save the mask for debugging
    save_path = "data/segmentation_mask.jpg"
    cv2.imwrite(save_path, binary_mask * 255)
    print(f"GrabCut segmentation mask saved to {save_path}")

    return binary_mask

# Keep the old function for non-interactive fallback if needed, or remove it.
# For now, let's keep it but rename the main one to be clear.
def segment_object(frame: np.ndarray) -> np.ndarray | None:
    return segment_object_interactive(frame)
