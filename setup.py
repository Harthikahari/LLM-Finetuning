"""Setup configuration for Text2SQL package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="text2sql",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Production-grade LLM fine-tuning for Text-to-SQL generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LLM-Finetuning",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/LLM-Finetuning/issues",
        "Documentation": "https://github.com/yourusername/LLM-Finetuning/blob/main/docs/index.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "text2sql-train=scripts.train:main",
            "text2sql-eval=scripts.evaluate:main",
            "text2sql-infer=scripts.inference:main",
        ],
    },
)
