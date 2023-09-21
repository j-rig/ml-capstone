try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="bizwiz",
    packages=find_packages(),
    package_dir={"bizwiz": "bizwiz"},
    install_requires=[
        "click",
        "requests",
        "Flask-Admin",
        "Flask-RESTful",
        "Flask-WTF",
        "Flask-Bootstrap",
        "Flask-BasicAuth",
        "Flask-SQLAlchemy",
        "SQLAlchemy",
        "joblib",
        "scikit-learn",
        "nltk",
        "beautifulsoup4",
        "extruct",
        "python-dotenv",
        "email_validator",
    ],
    entry_points={"console_scripts": ["bizwiz = bizwiz.cli:main"]},
    dependency_links=[],
)

# https://www.pythonanywhere.com/batteries_included/
