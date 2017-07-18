import pytest

from precessor import config


@pytest.fixture(autouse=True)
def patch_defaults(monkeypatch):
    monkeypatch.setattr(config, 'allowed_netlocs', ('example.com',))
    monkeypatch.setattr(config, 'allowed_extensions', {'jpg'})
    monkeypatch.setattr(config, 'cache_enabled', False)
    monkeypatch.setattr(config, 'debug', False)
