#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from bp import settings


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bp.settings')

    #Begin coverage custom part
    running_tests = (sys.argv[1] == 'test')
    if running_tests:
        from coverage import Coverage
        cov = Coverage()
        cov.erase()
        cov.start()
        settings.IS_TESTING = True
    #End coverage custom part

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    #Begin coverage custom part
    if running_tests:
        cov.stop()
        cov.save()
        covered = cov.report()
        if covered < 100:
            sys.exit(1)
    #End coverage custom part

if __name__ == '__main__':
    main()
