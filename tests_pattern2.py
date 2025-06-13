import pytest
from pattern_impl import Singleton

def test_singleton_instance():
# Демонстрация работы паттерна Singleton

    s1 = Singleton("Первое значение")
    print(f"s1 value: {s1.get_value()}")  # Ожидается: Первое значение

    s2 = Singleton("Второе значение")
    print(f"s2 value: {s2.get_value()}")  # Ожидается: Первое значение, т.к. инициализация только один раз

    print(f"s1 is s2: {s1 is s2}")  # True — обе переменные указывают на один объект

    s2.set_value("Новое значение")
    print(f"s1 value после изменения через s2: {s1.get_value()}")  # Новое значение


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
