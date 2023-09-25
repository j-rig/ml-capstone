try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="bizwiz",
    version="0.0.1",
    author="jrig",
    url="https://github.com/j-rig",
    author_email="jrighetti@alumni.ucsd.edu",
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
        "joblib==1.1.0",
        "scikit-learn==1.0.2",
        "nltk==3.6.7",
        "beautifulsoup4",
        "extruct",
        "python-dotenv",
        "email_validator",
    ],
    entry_points={"console_scripts": ["bizwiz = bizwiz.cli:main"]},
    dependency_links=[],
)
