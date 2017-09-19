from setuptools import setup, find_packages

setup(
    name='driloader',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Driver downloader for Selenium',
    author='Lucas Trajano;Felipe Viegas;Jonatha Daguerre',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
