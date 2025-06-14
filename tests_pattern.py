import pytest
from unittest.mock import patch, MagicMock
from pattern_impl import Logger
from unittest.mock import patch
import logging
import time
import os





def test_singleton_instance():
    logger1 = Logger("test.log")
    logger2 = Logger("other.log")
    assert logger1 is logger2
    assert logger1.get_log_file() == "test.log"
    assert logger2.get_log_file() == "test.log"

def test_logging_methods(capsys):
    # log_file = tmp_path / "app.log"
    # log_file.parent.mkdir(parents=True, exist_ok=True) 
    Logger._instance = None  # Сброс синглтона для изоляции теста
    logger = Logger("ignored.log", use_console=True)
    logger.log_info("Info message")
    logger.log_warning("Warning message")
    logger.log_error("Error message")

    # Flush handlers to ensure logs are written
    for handler in logger.logger.handlers:
        handler.flush()
        handler.close()
    logger.logger.handlers.clear()  # Очистка, чтобы не мешать другим тестам
    
    time.sleep(0.1)

    # print("Files in tmp_path:", os.listdir(tmp_path))
    # assert log_file.exists(), "Log file was not created"

    captured = capsys.readouterr()
    assert "Info message" in captured.err
    assert "Warning message" in captured.err
    assert "Error message" in captured.err



def test_invalid_log_file():
    # Сброс экземпляра синглтона для изолированного теста
    Logger._instance = None
    with pytest.raises(ValueError):
        Logger("")  # Пустая строка недействительна

    Logger._instance = None
    with pytest.raises(ValueError):
        Logger(None)  # Нет недействительных


def test_logger_with_mock_filehandler():
    Logger._instance = None  # Сброс синглтона

    real_file_handler = MagicMock()
    real_file_handler.level = logging.INFO  # Уровень должен быть int

    with patch("pattern_impl.logging.FileHandler", return_value=real_file_handler) as mock_file_handler:
        logger = Logger("mock.log", use_console=False)
        logger.log_info("Test message")

        mock_file_handler.assert_called_once_with("mock.log")
        real_file_handler.setFormatter.assert_called()


def test_thread_safety(tmp_path):
    import threading

    Logger._instance = None  # Сбросить синглтон

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

    # Все экземпляры должны быть одинаковыми
    first = instances[0]
    assert all(inst is first for inst in instances)
    assert first.get_log_file() == str(log_file)

