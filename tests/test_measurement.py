import pytest
from app.model.measurement import Measurement


@pytest.mark.parametrize("primerBatch,t_to,expected", [
    (1, 12.4, False),
    (1, 12.3, True),
    (2, 12.4, False),
    (2, 12.3, True),
    (3, 11.7, False),
    (3, 11.6, True),
    (4, 11.7, False),
    (4, 11.6, True),
    (5, 12.2, False),
    (5, 12.1, True),
    (5, 12.0, False),
])
def test_primerBatch_errorLowT_to(primerBatch, t_to, expected):
    out = Measurement(primerBatch=primerBatch, t_to=t_to)
    assert out.errorLowT_to == expected
