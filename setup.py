from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()
DESCRIPTION = 'Driver downloader for Selenium'
REQUIRED = ['certifi', 'chardet', 'idna', 'requests', 'urllib3']

setup(
    name='driloader',
    version='1.2.6',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={'driloader': ['drivers_info.ini']},
    install_requires=REQUIRED,
    include_package_data=True,
    author='Lucas Trajano; Felipe Viegas; Jonatha Daguerre',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing'
    ]
)
