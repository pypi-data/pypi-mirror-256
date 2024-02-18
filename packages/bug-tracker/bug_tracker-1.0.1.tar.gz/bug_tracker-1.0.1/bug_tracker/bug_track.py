import traceback
import sys
import requests, json
from django.conf import settings
import os
import platform
import socket
from django.core.exceptions import ImproperlyConfigured


class ConsoleExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = getattr(settings, 'CONSOLE_EXCEPTION_LOGGER_KEY', None)
        print(self.key)
        if not self.key:
            raise ImproperlyConfigured("CONSOLE_EXCEPTION_LOGGER_KEY is missing in settings.")

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, e)
            raise
        return response


    def process_exception(self, request, exception):

        # print(request.META.get("HTTP_USER_AGENT"),'000000000000000000000000000000000000000000000',self.key)
        browserName = request.META.get("HTTP_USER_AGENT")

        exc_info = sys.exc_info()
        version = sys.version

        value = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        print(value)
        uri = request.build_absolute_uri()

        base_dir = settings.BASE_DIR

        project_name = os.path.basename(base_dir)
        language = platform.python_implementation()
        url = "https://bugtracking.colanapps.in/api/bugtrack/"
        
        user = socket.gethostname()
        payload = json.dumps({
        "error": "test",
        "title": "testing",
        "description": value,
        "user": user,
        "url": uri,
        "python_version": version,
        "browser_name": browserName,
        "project_name": project_name,
        "language": language
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': self.key
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response)
