# src/output.py
import cv2
import numpy as np

def display_results(weight_grams: float, frame: np.ndarray, bbox: tuple | None):
    """
    Displays the final weight and overlays results on the frame.

    Args:
        weight_grams (float): The estimated weight in grams.
        frame (np.ndarray): The original image frame.
        bbox (tuple | None): The bounding box (x, y, w, h) of the object.
    """
    print(f"--- Final Result ---")
    print(f"Estimated Weight: {weight_grams:.2f} grams")
    print(f"--------------------")

    if frame is None:
        print("No frame to display.")
        return

    output_frame = frame.copy()

    # Draw bounding box if available
    if bbox:
        x, y, w, h = bbox
        cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Prepare text for display
    text = f"Weight: {weight_grams:.2f} g"
    text_position = (10, 30)

    # Draw the text on the image
    cv2.putText(
        output_frame,
        text,
        text_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    # Save the annotated frame
    save_path = "data/output_frame.jpg"
    cv2.imwrite(save_path, output_frame)
    print(f"Annotated output frame saved to {save_path}")

    # Display the image in a window
    cv2.imshow("Weight Estimation Result", output_frame)
    print("Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
