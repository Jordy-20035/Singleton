import pytest
from unittest.mock import patch, MagicMock
from pattern_impl import Logger
from unittest.mock import patch
import logging



def test_singleton_instance():
    logger1 = Logger("test.log")
    logger2 = Logger("other.log")
    assert logger1 is logger2
    assert logger1.get_log_file() == "test.log"
    assert logger2.get_log_file() == "test.log"

def test_logging_methods(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.parent.mkdir(parents=True, exist_ok=True) 
    logger = Logger(str(log_file))
    logger.log_info("Info message")
    logger.log_warning("Warning message")
    logger.log_error("Error message")

    # Flush handlers to ensure logs are written
    for handler in logger.logger.handlers:
        handler.flush()

    content = log_file.read_text()
    assert "Info message" in content
    assert "Warning message" in content
    assert "Error message" in content

def test_invalid_log_file():
    # Reset singleton instance for isolated test
    Logger._instance = None
    with pytest.raises(ValueError):
        Logger("")  # Empty string invalid

    Logger._instance = None
    with pytest.raises(ValueError):
        Logger(None)  # None invalid


def test_logger_with_mock_filehandler():
    Logger._instance = None  # Сброс синглтона

    real_file_handler = MagicMock()
    real_file_handler.level = 20  # Установим уровень, чтобы избежать TypeError

    with patch("pattern_impl.logging.FileHandler", return_value=real_file_handler) as mock_file_handler:
        logger = Logger("mock.log")
        logger.log_info("Test message")

        mock_file_handler.assert_called_with("mock.log")
        real_file_handler.setFormatter.assert_called()

def test_thread_safety(tmp_path):
    import threading

    Logger._instance = None  # Reset singleton

    log_file = tmp_path / "thread.log"
    instances = []

    def create_logger():
        logger = Logger(str(log_file))
        instances.append(logger)

    threads = [threading.Thread(target=create_logger) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All instances must be the same
    first = instances[0]
    assert all(inst is first for inst in instances)
    assert first.get_log_file() == str(log_file)

