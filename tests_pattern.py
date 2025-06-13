import pytest
from pattern_impl import Singleton

def test_singleton_instance():
    s1 = Singleton("first")
    s2 = Singleton("second")
    assert s1 is s2, "Singleton instances should be the same object"
    assert s1.get_value() == "first"
    assert s2.get_value() == "first"

def test_singleton_set_value():
    s = Singleton()
    s.set_value("new_value")
    assert s.get_value() == "new_value"

def test_singleton_reset(monkeypatch):
    # Monkeypatch _instance for isolation
    from pattern_impl import Singleton
    monkeypatch.setattr(Singleton, "_instance", None)
    s = Singleton("reset_value")
    assert s.get_value() == "reset_value"
