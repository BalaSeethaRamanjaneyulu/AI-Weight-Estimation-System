# src/main.py

from . import camera
from . import segmentation
from . import geometry
from . import scaling
from . import volume_engine
from . import density_engine
from . import output

def main():
    """
    Main function to run the weight estimation pipeline.
    """
    print("Starting AI Weight Estimation System...")

    # 1. Capture frame
    frame = camera.capture_frame()

    # 2. Segment object
    mask = segmentation.segment_object(frame)

    # 3. Calculate area
    area_pixels, bbox = geometry.calculate_area(mask)

    # 4. Get scale factor
    # For now, we use a manual scale factor to avoid unreliable reference object detection.
    # This value assumes a specific camera distance and resolution.
    MANUAL_SCALE_FACTOR = 0.05  # Example value: 1cm is 20 pixels -> 1/20 = 0.05 cm/pixel
    scale_factor = scaling.get_manual_scale_factor(MANUAL_SCALE_FACTOR)


    # 5. Calculate volume
    volume_cm3 = volume_engine.calculate_volume(mask, scale_factor)

    # 6. Get density
    density_g_cm3 = density_engine.get_density("apple") # Placeholder

    # 7. Calculate weight
    weight_grams = volume_cm3 * density_g_cm3

    # 8. Display result
    output.display_results(weight_grams, frame, bbox)

    print("Pipeline finished.")


if __name__ == "__main__":
    main()
