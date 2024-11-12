#!/usr/bin/env python
"""
Command-line utility for administrative tasks.

For more information about this file, visit
https://docs.djangoproject.com/en/2.1/ref/django-admin/
"""

import os
import sys

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paramCSbackend.settings')

def main():
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Debug information
    print("Python version:", sys.version)
    print("Python executable:", sys.executable)
    print("Current working directory:", os.getcwd())
    print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))
    print("sys.path:", sys.path)
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
