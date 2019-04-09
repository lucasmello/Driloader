class BrowserDetectionError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super(BrowserDetectionError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)


class BrowserNotSupportedError(Exception):
    """ BrowserDetectionError """
    def __init__(self, message, cause):
        """Init method
        Sets superclass arguments up.
        Sets the cause of exception up.
        """
        super(BrowserNotSupportedError, self).__init__(message)
        self.cause = cause

    def __str__(self):
        return 'Error: {}.\nCause: {}'.format(self.args[0], self.cause)
