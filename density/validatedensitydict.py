# density/validatedensitydict.py

from pydantic import ValidationError
from density.schemachecker.densityspec import DensitySpec


def validate_density_dict(data: dict) -> dict:
    """
    Validate a raw dict using the 'DensitySpec' union.
    Raises ValidationError if the data doesn't match the schema.
    Returns a normalized dict on success.
    """
    model = DensitySpec.model_validate(data)
    # model is a RootModel instance: model.root is the actual union variant
    return model.model_dump()


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
                    "name": "my_custom_dist",
                    "params": {"alpha": 2.0}
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
