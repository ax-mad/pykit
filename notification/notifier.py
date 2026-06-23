
class Notifier:
    """
    Multiple protocols in the future such as SMS, and Ntfy,
    for now, only implementing ntfy
    """
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
