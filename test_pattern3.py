## Тест с mock-объектом

import pytest
from pattern_impl import Singleton

def test_singleton_instance():
    s1 = Singleton("Первое значение")
    s2 = Singleton("Второе значение")
    assert s1 is s2
    assert s1.get_value() == "Первое значение"

def test_singleton_set_value():
    s = Singleton()
    s.set_value("new_value")
    assert s.get_value() == "new_value"

def test_singleton_reset(monkeypatch):
    monkeypatch.setattr(Singleton, "_instance", None)
    s = Singleton("reset_value")
    assert s.get_value() == "reset_value"
