def test_singleton(test_runner_service_account_credentials):

    from helpers import configuration
    from helpers import _Configuration

    instance = _Configuration()
    assert isinstance(instance, _Configuration)
    instance = _Configuration()

    assert instance is configuration

    class Toto(_Configuration):
        def __init__(self) -> None:
            assert not hasattr(self, "dummy")

    # test the Toto constructor is called one time
    instance = Toto()
    instance.dummy = True
    instance = Toto()


def test_dataset(test_runner_service_account_credentials):

    import helpers

    dataset = helpers.configuration.DATASET

    assert dataset == "orange"


def test_class_property(test_runner_service_account_credentials):

    from helpers import _Configuration

    dataset = _Configuration().DATASET

    assert dataset == "orange"
