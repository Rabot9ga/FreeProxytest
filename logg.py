import logging

class ColoredFormatter(logging.Formatter):
    """Formatter for colored output"""
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
              'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}

    def format(self, record):
        log_fmt = (f"{self.COLORS.get(record.levelname, '')} 📊 %(levelname)s - ⏳ %(asctime)s - "
                   f"⚠️ %(funcName)s - 📝 line: %(lineno)d - 💬 %(message)s\033[0m")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
