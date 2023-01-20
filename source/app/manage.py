#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

    """Detect environment file .env and load"""
    path_env = ""
    if sys.argv:
        for i in range(len(sys.argv)):
            if (sys.argv[i] == "--path_env"):
                path_env = sys.argv[i + 1]
                sys.argv.pop(i)
                sys.argv.pop(i)
                break

    from dotenv import load_dotenv
    path = os.path.abspath(path_env + ("/" if path_env != "" else "") + ".env") 
    from os.path import exists
    if path:
        file_exists = exists(path)
        if (not file_exists):
            print("ERROR: ENV " + path + " not found")
        else:
            print("INFO: ENV " + path + " found")
            
    load_dotenv(path)

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
