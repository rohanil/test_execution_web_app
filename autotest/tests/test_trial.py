import time


def test_sample_successful():
    time.sleep(3)
    assert 1 == 1


def test_sample_failing():
    time.sleep(3)
    assert 1 == 2
