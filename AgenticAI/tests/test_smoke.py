def test_package_importable():
    import importlib
    module = importlib.import_module('my_crewai_project')
    assert hasattr(module, 'Agent')
