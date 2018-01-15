from hpsearch import parameter

def test_simple_spec():
    spec = {
        'parameterName': 'foo',
        'type': 'INTEGER',
        'scaleType': 'UNIT_LINEAR_SCALE',
        'minValue': 10,
        'maxValue': 100
    }
    sampler = parameter.ParameterSampler(spec)
    assert sampler.name == 'foo'
    samples = [sampler.sample() for _ in range(100)]
    assert all(x >= 10 for x in samples)
    assert all(x <= 100 for x in samples)

