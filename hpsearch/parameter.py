import math
import random

def _double_linear(minimum, maximum):
    return random.uniform(minimum, maximum)

def _double_log(minimum, maximum):
    a = math.log(minimum)
    b = math.log(maximum)
    return math.exp(random.uniform(a, b))

def _integer_linear(minimum, maximum):
    return random.choice(range(minimum, maximum+1))

def _integer_log(minimum, maximum):
    return int(_double_log(minimum, maximum))

def _categorical(options):
    return random.choice(options)


class ParameterType(object):
    DOUBLE = "DOUBLE"
    INTEGER = "INTEGER"
    CATEGORICAL = "CATEGORICAL"

class ScaleType(object):
    NONE = "NONE"
    LINEAR = "UNIT_LINEAR_SCALE"
    LOG = "UNIT_LOG_SCALE"

def get_sample_fn_from_spec(param_spec):
    param_type = param_spec['type']
    scale_type = param_spec['scaleType']
    if (param_type, scale_type) == (ParameterType.DOUBLE, ScaleType.LINEAR):
        return lambda: _double_linear(param_spec['minValue'], param_spec['maxValue'])
    if (param_type, scale_type) == (ParameterType.DOUBLE, ScaleType.LOG):
        return lambda: _double_log(param_spec['minValue'], param_spec['maxValue'])
    if (param_type, scale_type) == (ParameterType.INTEGER, ScaleType.LINEAR):
        return lambda: _integer_linear(param_spec['minValue'], param_spec['maxValue'])
    if (param_type, scale_type) == (ParameterType.INTEGER, ScaleType.LOG):
        return lambda: _integer_log(param_spec['minValue'], param_spec['maxValue'])
    if param_type == ParameterType.CATEGORICAL:
        return lambda: _categorical(param_spec['categoricalValues'])

    raise ValueError("Invalid ParameterSpec")


class ParameterSampler(object):
    """ Creates a sampler from a ParameterSpec. """
    def __init__(self, param_spec):
        self.name = param_spec['parameterName']
        self.type = param_spec['type']
        self.param_spec = param_spec
        self.sample_fn = get_sample_fn_from_spec(param_spec)

    def sample(self):
        """ Returns a parameter value. """
        return self.sample_fn()
