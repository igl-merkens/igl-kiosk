"""Setup script for Fullscreen Web Display."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fullscreen-web-display",
    version="0.0.1",
    author="Maximilian Erkens",
    author_email="max@max-erkens.de",
    description="A PyQt6-based fullscreen web browser with external URL injection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maxjr2/fullscreen-web-display",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fullscreen-web-display=fullscreen_web_display.main:main",
        ],
    },
    keywords="qt pyqt6 browser fullscreen web display kiosk",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fullscreen-web-display/issues",
        "Source": "https://github.com/yourusername/fullscreen-web-display",
    },
)