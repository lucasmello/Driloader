"""
Responsible to keep proxy configurations.
"""


class Proxy:

    """
    Responsible to keep proxy configurations.
    """

    __instance = None

    def __new__(cls, proxy):
        if Proxy.__instance is None:
            Proxy.__instance = object.__new__(cls)
        Proxy.__instance.proxy = proxy
        return Proxy.__instance
