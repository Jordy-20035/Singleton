import logging
import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, log_file="app.log"):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file):
        if not hasattr(self, 'logger'):
            if not log_file or not isinstance(log_file, str):
                raise ValueError("log_file must be a non-empty string")
            self.logger = logging.getLogger("AppLogger")
            self.logger.setLevel(logging.INFO)
            # Avoid adding multiple handlers if _initialize called multiple times
            if not self.logger.handlers:
                file_handler = logging.FileHandler(log_file)
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            self._log_file = log_file

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def get_log_file(self):
        return getattr(self, '_log_file', None)

