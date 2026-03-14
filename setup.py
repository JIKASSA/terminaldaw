from setuptools import setup, find_packages

setup(
    name="terminaldaw",
    version="0.1.0",
    author="Joshua Vanzanella",
    description="Control Ableton Live from the terminal via OSC and Live Object Model",
    packages=find_packages(),
    install_requires=["python-osc"],
    entry_points={
        "console_scripts": [
            "terminaldaw=terminaldaw.cli:main",
        ]
    },
    python_requires=">=3.8",
)
