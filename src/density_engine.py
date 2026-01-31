# src/density_engine.py
import json

DENSITY_DB_PATH = "data/density_db.json"

def get_density(object_type: str) -> float:
    """
    Fetches the density for a given object type from the density database.

    Args:
        object_type (str): The type of object (e.g., "apple").

    Returns:
        float: The density of the object in g/cm^3.
    """
    print(f"Looking up density for object type: '{object_type}'")
    try:
        with open(DENSITY_DB_PATH, 'r') as f:
            density_db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not read density database at {DENSITY_DB_PATH}. {e}")
        print("Falling back to default density (1.0 g/cm^3).")
        return 1.0

    object_data = density_db.get(object_type.lower())

    if object_data:
        density = object_data.get("density_g_cm3", 1.0)
        print(f"Found density: {density} g/cm^3")
        return density
    else:
        print(f"Warning: Object type '{object_type}' not found in density database.")
        default_density = density_db.get("default", {}).get("density_g_cm3", 1.0)
        print(f"Falling back to default density: {default_density} g/cm^3")
        return default_density
