#!/usr/bin/env python
import os
import sys
import atexit

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Test.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    if "test" in sys.argv:
        from django.conf import settings
        source = [arg for arg in sys.argv[sys.argv.index("test"):] if arg in settings.INSTALLED_APPS]
        if not source:
            source = settings.INSTALLED_APPS[0:1]
        omit=list(set(settings.INSTALLED_APPS)-set(source))
        print(source)
        print(omit)
        import coverage
        cov = coverage.coverage(source=source, omit=[])
        cov.source = source
        cov.omit = []
        cov.erase()  # Erase previous reports
        cov.start()

        def stop_coverage():
            cov.stop()
            cov.save()
            print(cov.report())
            cov.html_report()

        atexit.register(stop_coverage)
    
    execute_from_command_line(sys.argv)
