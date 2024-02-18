"""Analysis utilities."""

import numpy as np


def create_axis(sweep_type, start, stop, steps=None, step_size=None):
    SWEEP_TYPES = {
        "lin": "linear",
        "linear": "linear",
        "log": "logarithmic",
        "logarithmic": "logarithmic"
    }

    SWEEP_FUNCS = {
        ("linear", "steps"): np.linspace,
        ("linear", "step_size"): np.arange,
        ("logarithmic", "steps"): np.geomspace,
        ("logarithmic", "step_size"): np.logspace,
    }

    try:
        sweep_type = SWEEP_TYPES[sweep_type.casefold()]
    except KeyError:
        raise ValueError(f"unrecognised sweep type {repr(sweep_type)}")

    start = float(start)
    stop = float(stop)

    if not (steps is None) ^ (step_size is None):
        raise ValueError("exactly one of steps and step_size must be specified")
    elif steps is None:
        step_size = float(step_size)

        if sweep_type == "linear":
            return np.arange(start, stop + 1, step_size)
        else:
            raise ValueError("logarithmic axes have not concept of a `step_size` (use `steps`)")
    else:
        steps = int(steps)

        if sweep_type == "linear":
            return np.linspace(start, stop, steps)
        else:
            return np.geomspace(start, stop, steps)
