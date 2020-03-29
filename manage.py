#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # switch settings for development and production: choose one DJANGO_SETTINGS_MODULE from below to run
    # Additional work for Pycharm settings: Files->Settings->Language&Frameworks->Django -> change 'Settings'
    # location to slinky/settings/development.py or slinky/settings/production.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slinky.settings.development')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slinky.settings.production')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
