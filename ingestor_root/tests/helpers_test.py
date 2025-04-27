def test_dataset():

    import helpers

    dataset = helpers.configuration.DATASET

    assert dataset == "orange"


def test_class_property():

    from helpers import _Configuration

    dataset = _Configuration().DATASET

    assert dataset == "orange"
