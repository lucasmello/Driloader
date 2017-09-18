# Driloader
.. image:: https://img.shields.io/pypi/v/driloader.svg
    :target: https://pypi.python.org/pypi/driloader

.. image:: https://img.shields.io/pypi/l/driloader.svg
    :target: https://pypi.python.org/pypi/driloader

.. image:: https://img.shields.io/pypi/pyversions/driloader.svg
    :target: https://pypi.python.org/pypi/driloader

.. image:: https://img.shields.io/github/contributors/lucasmello/Driloader.svg
    :https://github.com/lucasmello/Driloader/graphs/contributors

Selenium drivers downloader tool with standalone CLI support.

 **Why is it for?**
 
 Selenium needs a specific driver to work with each browser. Every driver has a version that works with specific browser
 versions, and it's really annoying reading the changelogs to check if the current driver will work with the new browser
 version. Plus, a lot of times a test crashes because the browser has updated and the driver is not compatible anymore.
 That's why Driloader exists: To make this process so much easier! Seriously, you don't need to worry with it anymore,
 we solved this problem!


**Requires:**
* Python 3.6 or higher

**Installing:**
```
 pip install driloader
```

**CLI Usage:**
```bash
chmod +x cli.py
./cli.py -h
```

Usage with Firefox:
```python
from driloader import driloader
from selenium.webdriver import Firefox

driver_path = driloader.download_gecko_driver()
browser = Firefox(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

Usage with Chrome
```python
from driloader import driloader
from selenium.webdriver import Chrome

driver_path = driloader.download_chrome_driver()
browser = Chrome(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

Usage with Internet Explorer
```python
from driloader import driloader
from selenium.webdriver import Ie

driver_path = driloader.download_ie_driver()
browser = Ie(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

Standalone usage:
```bash
cli.py [-h] (--firefox | --chrome | --internet-explorer | --all)
```

```bash
optional arguments:
  -h, --help            show this help message and exit
  --firefox, -f         get Firefox version.
  --chrome, -c          get Google Chrome version.
  --internet-explorer, -i
                        get Internet Explorer version.
  --all                 look for browsers an get their versions.
```
***Get Firefox version***
```bash
$  ./cli.py --firefox
45
```

***Get Google Chrome version***
```bash
$  ./cli.py --chrome
58
```
''
***Get Internet Explorer version (Windows system)***
```cmd
> cli.py -i
11
```


***Get Internet Explorer version (non-Windows system)***
```bash
# Getting from a non-Windows system
$  ./cli.py --internet-explorer
Error: Unable to get the Internet Explorer version.
        Cause: Error: Unable to retrieve IE version..
        Cause: System is not Windows.
```

***Get all browsers version (non-Windows system)***
```bash
# Getting from a non-Windows system
$  ./cli.py --all
Internet Explorer: Error: Unable to get the Internet Explorer version.
        Cause: Error: Unable to retrieve IE version..
        Cause: System is not Windows.
Firefox: 45
Google Chrome: 58

```

***Get all browsers version (Windows system)***
```bash
> cli.py --all
Internet Explorer: 11
Firefox: 45
Google Chrome: 58

```

***If the browser is not found***
```bash
$  ./cli.py --chrome
Error: Unable to get the Google Chrome version.
        Cause: Error: Unable to retrieve Chrome version from system.
        Cause: Command "google-chrome --product-version" not found!
```
