from os import getenv

# ALTERNATIVE:

def env(key, required=False, validator=None, default=None):
    return {
        "key": key,
        "required": required,
        "validator": validator,
        "default": default,
    }


# class Configurator:
#     def __init__(self, **kwargs):
#         for attr, spec in kwargs.items():
#             if isinstance(spec, dict) and "key" in spec:
#                 setattr(self, attr, self.load_env(
#                     spec["key"],
#                     required=spec.get("required", False),
#                     validator=spec.get("validator"),
#                     default=spec.get("default")
#                 ))
#             else:
#                 setattr(self, attr, spec)

#     def load_env(self, key, required=False, validator=None, default=None):
#         value = os.getenv(key, default)
#         if required and not value:
#             raise ValueError(f"{key} IS REQUIRED")
#         if validator and value is not None and not validator(value):
#             raise ValueError(f"{key} HAS FAILED VALIDATION")
#         return value

#     def load_file(self, path, required=False, validator=None):
#         raise NotImplementedError("load_file not yet implemented")

# old
class Configurator:
    def __init__(self):
        self.caldav_url = self.load_env("CALDAV_URL", required=True)
        self.username   = self.load_env("CALDAV_USER", required=True)
        self.password   = self.load_env("CALDAV_PASS", required=True)
        self.api_key    = self.load_env("CALDAV_API_KEY", required=True) # validator=lambda v: len(v) >= 32

    def load_env(self, key:str, required=False, validator=None):
        value = getenv(key)
        if required and not value: raise ValueError(f"{key} IS REQUIRED")
        if validator and not validator(value): raise ValueError(f"{key} HAS FAILED VALIDATION")
        log(f"LOADED {key}")
        return value

    def load_file(self, filename:str, required:bool = False, validator = None):
        log(msg=f"NOT IMPLEMENTED. LOCATE {filename}, DOING VALIDATION, ETC ETC.....")
