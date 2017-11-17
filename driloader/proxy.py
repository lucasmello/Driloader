# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=too-few-public-methods

"""
driloader.proxy
------------------

Proxy is responsible for keeping proxy configurations for the whole module.
This singleton class must be assigned to a variable using the `url` argument only once.
The next assignments must use no arguments and then, the previously assigned value will be used.

Example of usage:
>>> from proxy import Proxy
>>> proxy = Proxy({'http': 'http://proxy.company.com:3128',
                   'https': 'http://proxy.company.com:3128'})
>>> proxy.urls
'http://proxy.company.com:3128'
>>> proxy
<proxy.Proxy object at 0x7fd6df1797b8>
>>> proxy2 = Proxy()
>>> proxy2
<proxy.Proxy object at 0x7fd6df1797b8>
>>> proxy2.urls
{'http': 'http://proxy.company.com:3128', 'https': 'http://proxy.company.com:3128'}
>>> Proxy().urls
{'http': 'http://proxy.company.com:3128', 'https': 'http://proxy.company.com:3128'}
"""


class Proxy:
    """
    Singleton class to store the proxy configuration. It must be
    initialized in when the main driloader module is called.

    __instance: class variable to store the only class instance.
    """
    __instance = None

    def __new__(cls, urls=None):
        """
        Static function responsible for creating a new instance of Proxy.
        This implementation aims to create a single instance of Proxy in the first
        assignment and then only return this instance.

        This current implementation doesn't allow multiple assignments to Proxy.
        Once assigned, the instance will not take a new value, unless explicitly set by
        using `instance_variable.url = 'new value'`

        :param urls: The proxy url in the format [http|https]://[HOST]:[PORT].
        """
        if Proxy.__instance is None:
            Proxy.__instance = object.__new__(cls)
            Proxy.__instance.urls = urls

        return Proxy.__instance
