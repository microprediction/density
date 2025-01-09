# example_usage.py

from density.validatedensitydict import validate_density_dict
from pydantic import ValidationError


if __name__ == "__main__":
    mixture_spec = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 0, "scale": 1}
                },
                "weight": 0.6
            },
            {
                "density": {
                    "type": "builtin",
                    "name": "normal",
                    "params": {"mu": 2.0, "sigma": 1.0}
                },
                "weight": 0.4
            }
        ]
    }
    try:
        validated_mixture = validate_density_dict(mixture_spec)
        print("Validated mixture:", validated_mixture)
    except ValidationError as e:
        print("Validation error in mixture:", e)
