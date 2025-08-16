from setuptools import setup, find_packages

setup(
    name="jobpilot",
    version="0.1.0",
    packages=find_packages(include=["job_agent", "dropin"]),
    install_requires=[],  # requirements.txt is used for dependencies
)
