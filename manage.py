#!/usr/bin/env python
import os
import sys


def main():
    # где лежат настройки
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.db_settings')

    # src в pythonpath
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django не установлен") from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()