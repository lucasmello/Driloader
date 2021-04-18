"""
Module that provides all needed custom exceptions.
"""


class BrowserDetectionError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super().__init__(message)
        self.cause = cause


class BrowserNotSupportedError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super().__init__(message)
        self.cause = cause
