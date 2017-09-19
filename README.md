# Driloader

[![pypi version](https://img.shields.io/pypi/v/driloader.svg)](https://pypi.python.org/pypi/driloader) [![license](https://img.shields.io/pypi/l/driloader.svg)](https://pypi.python.org/pypi/driloader) [![python versions](https://img.shields.io/pypi/pyversions/driloader.svg)](https://pypi.python.org/pypi/driloader) [![contributors](https://img.shields.io/github/contributors/lucasmello/Driloader.svg)](https://github.com/lucasmello/Driloader/graphs/contributors)

Selenium drivers downloader tool with standalone CLI support.

 ## Why is it for?
 
 Selenium needs a specific driver to work with each browser. Every driver has a version that works with specific browser
 versions, and it's really annoying reading the changelogs to check if the current driver will work with the new browser
 version. Plus, a lot of times a test crashes because the browser has updated and the driver is not compatible anymore.
 That's why Driloader exists: To make this process so much easier! Seriously, you don't need to worry about it anymore,
 we solved this problem!

## Requires
* Python 3.6 or higher

## Installing
```
 pip install driloader
```

## Usage with Firefox
```python
from driloader import driloader
from selenium.webdriver import Firefox

driver_path = driloader.download_gecko_driver()
browser = Firefox(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

## Usage with Chrome
```python
from driloader import driloader
from selenium.webdriver import Chrome

driver_path = driloader.download_chrome_driver()
browser = Chrome(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

## Usage with Internet Explorer
```python
from driloader import driloader
from selenium.webdriver import Ie

driver_path = driloader.download_ie_driver()
browser = Ie(executable_path=driver_path)
browser.get("http://www.google.com")
browser.quit()
```

## CLI and standalone usage
```bash
chmod +x cli.py
./cli.py -h

usage: cli.py [-h] (--firefox | --chrome | --internet-explorer | --all)

optional arguments:
  -h, --help            show this help message and exit
  --firefox, -f         get Firefox version.
  --chrome, -c          get Google Chrome version.
  --internet-explorer, -i
                        get Internet Explorer version.
  --all                 look for browsers an get their versions.
```
### Retrieve Firefox version
```bash
$  ./cli.py --firefox
45
```

### Retrieve Google Chrome version
```bash
$  ./cli.py --chrome
58
```

### Retrieve Internet Explorer version (Windows system)
```cmd
> cli.py -i
11
```

### Retrieve all browsers version (Windows system)
```bash
> cli.py --all
Internet Explorer: 11
Firefox: 45
Google Chrome: 58

```

### Retrieve all browsers version (non-Windows system)
```bash
# Getting from a non-Windows system
$  ./cli.py --all
Internet Explorer: Error: Unable to get the Internet Explorer version.
        Cause: Error: Unable to retrieve IE version..
        Cause: System is not Windows.
Firefox: 45
Google Chrome: 58

```
