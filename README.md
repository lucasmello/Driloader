# Driloader
Selenium drivers downloader tool with standalone CLI support.


**Requires:**
* Python 3.4 or higher

**CLI Usage:**
```bash
chmod +x cli.py
./cli.py -h
```

usage:
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
