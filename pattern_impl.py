import logging
import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, log_file="app.log", use_console=False):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(log_file, use_console)
        return cls._instance

    def _initialize(self, log_file, use_console):
        if not hasattr(self, 'logger'):
            if not log_file or not isinstance(log_file, str):
                raise ValueError("log_file must be a non-empty string")
            self.logger = logging.getLogger("AppLogger")
            self.logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            if use_console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
            else:
                file_handler = logging.FileHandler(log_file)
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

