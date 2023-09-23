try:
    from setuptools import setup, find_packages, find_namespace_packages
except ImportError:
    from distutils.core import setup, find_packages, find_namespace_packages

setup(
    name="bizwiz",
    packages=find_packages(),
    # packages=find_namespace_packages(where= "bizwiz"),
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
        "scikit-learn",
        "nltk",
        "beautifulsoup4",
        "extruct",
        "python-dotenv",
        "email_validator",
    ],
    entry_points={"console_scripts": ["bizwiz = bizwiz.cli:main"]},
    dependency_links=[],
    # include_package_data=True,
    # package_data={ "bizwiz.data":["*.joblib",],
    # "bizwiz.static":["*.jpg",],
    # "bizwiz.templates":["*.html",],
    # }
    # package_data={
    #     "": [
    #         "data/*.joblib",
    #         "static/*.jpg",
    #         "static/*.css",
    #         "static/*.js",
    #         "templates/*.html",
    #     ]
    # },
)

# https://www.pythonanywhere.com/batteries_included/
