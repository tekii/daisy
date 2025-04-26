from tekii.margot.toolbox.singleton import Singleton


def test_singleton():
    class TestSingletonClass(metaclass=Singleton):
        pass

    instance1 = TestSingletonClass()
    instance2 = TestSingletonClass()

    assert instance1 is instance2
