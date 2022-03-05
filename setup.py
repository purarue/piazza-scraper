from pathlib import Path
from setuptools import setup, find_packages

requirements = Path("requirements.txt").read_text().splitlines()

pkg = "piazza_scraper"
setup(
    name=pkg,
    version="0.1.0",
    license="MIT",
    packages=find_packages(include=[pkg]),
    package_data={pkg: ["py.typed"]},
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={"console_scripts": ["piazza_scraper = piazza_scraper.__main__:main"]},
)
