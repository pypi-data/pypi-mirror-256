import logging
import sys
import re
from logging.handlers import RotatingFileHandler
import os
import site
from datetime import datetime

HTML_LOG_HEAD = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>логи</title><style>html, body{background-color:#1d1e22; color:#c1beb4; font-family: monospace;}div{white-space: pre-line;}.start{color:#97b270}.msg{color:#70a9b2;}.error{font-weight: bolder; color:#b27070;}.trace{color:#b29e9e;}</style></head><body>'


class Logger:
    def __init__(self, log_file, logging_level: str = 'WARN'):
        self.log_file = log_file
        self.logging_level = logging_level
        self.red = "\033[01;38;05;203m"
        self.green = "\033[01;38;05;40m"
        self.blue = "\033[01;38;05;74m"
        self.yellow = "\033[01;38;05;221m"
        self.redblack = "\033[01;38;05;204;48;05;232m"
        self.turquoise = "\033[01;38;05;80m"
        self.usual = "\033[0m"
        self.log_lvl = getattr(logging, self.logging_level)
        event_level = 35
        self.event_level = event_level

        def event(self, message, *args, **kwargs):
            if self.isEnabledFor(event_level):
                self._log(event_level, message, args, **kwargs)

        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_lvl)
        logging.addLevelName(logging.WARNING, 'ПРЕДУПРЕЖДЕНИЕ')
        logging.addLevelName(logging.ERROR, 'ОШИБКА')
        logging.addLevelName(logging.CRITICAL, 'ОПАСНОСТЬ')
        logging.addLevelName(logging.INFO, 'ИНФОРМАЦИЯ')
        logging.addLevelName(logging.DEBUG, 'ОТЛАДКА')
        logging.Logger.event = event
        logging.addLevelName(self.event_level, "СОБЫТИЕ")
        colors = {
            'ПРЕДУПРЕЖДЕНИЕ': self.yellow,
            'ОШИБКА': self.red,
            'ОПАСНОСТЬ': self.redblack,
            'ИНФОРМАЦИЯ': self.green,
            'ОТЛАДКА': self.blue,
            'СОБЫТИЕ': self.turquoise,
            'ТЕКСТ': self.usual
        }

        class SensitiveInfoFilter(logging.Filter):
            def filter(self, record):
                original_message = record.getMessage()
                clean_message = re.sub(r'https://api.telegram.org/bot[\w\-]+/', 'BotAPI:', original_message)
                clean_message = clean_message.replace(" СОБЫТИЕ :", "")
                record.msg = clean_message
                return True

        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                levelname = record.levelname
                if levelname in colors:
                    record.levelname = colors[levelname] + levelname + "\033[0m"
                return super().format(record)

        class UsualFormatter(logging.Formatter):
            def format(self, record):
                message = record.getMessage()
                for color in colors.values():
                    message = message.replace(color, '')
                record.msg = message
                return super().format(record)

        formatter = ColoredFormatter('%(asctime)s | %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        file_format = UsualFormatter('%(asctime)s | %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=10, encoding='utf-8')
        file_handler.setLevel(self.log_lvl)
        file_handler.addFilter(SensitiveInfoFilter())
        file_handler.setFormatter(file_format)
        logger_handler = self.CustomHandler(log_file)
        logger_handler.setFormatter(formatter)
        self.logger.addHandler(logger_handler)
        stream_handler = logger_handler
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(SensitiveInfoFilter())
        logger_handler.setLevel(self.log_lvl)
        self.logger.addHandler(stream_handler)
        stream_handler.setLevel(self.log_lvl)
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_lvl)
        self.logger.addHandler(file_handler)
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.event = self.logger.event
        self.warn = self.logger.warning
        self.error = self.logger.error
        self.crit = self.logger.critical
        self.exception = self.logger.exception
        sys.excepthook = self.handle_exception

    class CustomHandler(logging.StreamHandler):
        def __init__(self, log_file):
            super().__init__()
            self.log_file = log_file
            self.ignore = ['getUpdates', 'sendChatAction']

        def emit(self, record):
            if any(action in record.getMessage() for action in self.ignore):
                record.levelno = logging.DEBUG
                record.levelname = logging.getLevelName(record.levelno)
                return
            new_record = logging.LogRecord(
                record.name,
                record.levelno,
                record.pathname,
                record.lineno,
                record.msg,
                record.args,
                record.exc_info,
                record.funcName
            )
            super().emit(new_record)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("ПОЛНЫЙ ПРОЛАПС", exc_info=(exc_type, exc_value, exc_traceback))

    def log_to_html(self, log_file: str | None = None) -> str:
        log_file = self.log_file if not log_file else log_file
        for filename in os.listdir(os.path.dirname(log_file)):
            if os.path.splitext(filename)[1] == '.html':
                os.remove(os.path.join(os.path.dirname(log_file), filename))

        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        start_index = 0
        for i in range(len(lines) - 1, -1, -1):
            if "СТАРТ: " in lines[i]:
                start_index = i - 1
                break
        html_lines = [f"{HTML_LOG_HEAD}<div class='lvl'>уровень логгирования: {self.logging_level}</div>"]
        trace_flag = False
        msg_flag = False
        for line in lines[start_index:]:
            if "СТАРТ: " in line:
                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                html_lines.append('<div class="start">\n')
                html_lines.append(lines[start_index])
                html_lines.append(line)
                html_lines.append(lines[start_index + 2])
                html_lines.append('</div>\n')
            elif "ПРЕДУПРЕЖДЕНИЕ : " in line or "ИНФОРМАЦИЯ : " in line or "ОТЛАДКА : " in line or "ОПАСНОСТЬ : " in line:
                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                if trace_flag:
                    html_lines.append('</div>\n')
                    trace_flag = False
                if "ПРЕДУПРЕЖДЕНИЕ : " in line:
                    html_lines.append('<div class="warn">' + line + '</div>\n')
                elif "ИНФОРМАЦИЯ : " in line:
                    html_lines.append('<div class="info">' + line + '</div>\n')
                elif "ОТЛАДКА : " in line:
                    html_lines.append('<div class="debug">' + line + '</div>\n')
                elif "ОПАСНОСТЬ : " in line:
                    html_lines.append('<div class="crit">' + line + '</div>\n')
            elif "ОШИБКА : " in line:
                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                if trace_flag:
                    html_lines.append('</div>\n')
                    trace_flag = False
                html_lines.append('<div class="error">' + line + '</div>\n<div class="trace">')
                trace_flag = True
            elif trace_flag and not re.search(r'\s\|\s', line):
                html_lines.append(line)
            else:
                if trace_flag:
                    html_lines.append('</div>\n')
                    trace_flag = False
                if not msg_flag and not re.search(r'----+', line):
                    html_lines.append('<div class="msg">\n' + line)
                    msg_flag = True
                elif not re.search(r'----+', line):
                    html_lines.append(line)
        if msg_flag:
            html_lines.append('</div>\n')
        if trace_flag:
            html_lines.append('</div>\n')
        html_lines.append('</body></html>')
        html_code = []
        for line in html_lines:
            for pip_path in site.getsitepackages():
                line = line.replace(pip_path[0].upper() + pip_path[1:].replace('\\\\', '\\') if os.name == 'nt' else pip_path, '...')
            html_code.append(line)
        last_log_html = os.path.join(os.path.split(log_file)[0], os.path.splitext(os.path.split(log_file)[1])[0] + '_{:%d.%m.%Y_%H-%M-%S}.html').format(datetime.now())
        with open(last_log_html, 'w', encoding='utf-8') as file:
            file.writelines(html_code)
        return last_log_html


