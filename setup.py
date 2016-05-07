from setuptools import setup, find_packages
from tsuru_dashboard import __version__


setup(
    name="tsuru_dashboard",
    url="https://github.com/tsuru/tsuru-dashboard",
    version=__version__,
    packages=find_packages(),
    description="Web dashboard for tsuru PaaS",
    author="tsuru",
    author_email="tsuru@corp.globo.com",
    include_package_data=True,
    install_requires=[
        "Django>=1.9.6",
        "requests>=2.8.1",
        "python-dateutil>=2.4.2",
        "pytz>=2015.4",
        "Pygments>=2.0.2",
        "tsuruclient>=0.2.1",
        "grequests>=0.2.0",
    ],
)
