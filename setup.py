import setuptools
import versioneer


with open('DESCRIPTION.md', 'r') as desc:
    long_description = desc.read()

setuptools.setup(
    name="flake8-reports",
    license="MIT",
    version=versioneer.get_version(),
    description='This package provides formatting XML, JSON, and JUnit for flake8', # noqa
    long_description=long_description,
    author="Karthik Nadig",
    author_email="karthiknadig@gmail.com",
    url="https://github.com/karthiknadig/flake8-reports",
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    packages=["flake8_reports", ],
    package_dir={'': 'src'},
    install_requires=["flake8 > 3.0.0", ],
    entry_points={
        'flake8.report': [
            'junit = flake8_reports:Flake8junit',
            'xml = flake8_reports:Flake8xml',
            'csv = flake8_reports:Flake8csv',
            'tsv = flake8_reports:Flake8tsv',
            'ssv = flake8_reports:Flake8ssv',
            'json = flake8_reports:Flake8json',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    cmdclass=versioneer.get_cmdclass(),
)
