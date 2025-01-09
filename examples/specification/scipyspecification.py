# example_usage.py

from density.validatedensitydict import validate_density_dict
from pydantic import ValidationError


if __name__ == "__main__":
    # Quick example usage
    spec = {
        "type": "scipy",
        "name": "norm",
        "params": {"loc": 0, "scale": 1}
    }
    try:
        validated = validate_density_dict(spec)
        print("Validated single density:", validated)
    except ValidationError as e:
        print("Validation error:", e)

