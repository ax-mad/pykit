from os import getenv

class Configurator:
    def __init__(self, **kwargs):
        for attr, spec in kwargs.items():
            if isinstance(spec, dict) and "key" in spec:
                setattr(self, attr, self.load_env(
                    spec["key"],
                    required=spec.get("required", False),
                    validator=spec.get("validator"),
                    default=spec.get("default")
                ))
            else:
                setattr(self, attr, spec)

    def load_env(self, key, required=False, validator=None, default=None):
        value = getenv(key, default)
        if required and not value:
            raise ValueError(f"{key} IS REQUIRED")
        if validator and value is not None and not validator(value):
            raise ValueError(f"{key} HAS FAILED VALIDATION")
        return value

    def load_file(self, path, required=False, validator=None):
        raise NotImplementedError("load_file not yet implemented")

def env(key, required=False, validator=None, default=None):
    return {
        "key": key,
        "required": required,
        "validator": validator,
        "default": default,
    }
