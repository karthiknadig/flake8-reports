import setuptools
import versioneer


with open('DESCRIPTION.md', 'r') as desc:
    description = desc.read()

setuptools.setup(
    name="flake8reports",
    license="MIT",
    version=versioneer.get_version(),
    description=description,
    long_description_content_type='text/markdown',
    author="Karthik Nadig",
    url="https://gitlab.com/karthiknadig/flake8reports",
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    packages=["flake8reports",],
    package_dir={'': 'src'},
    install_requires=["flake8 > 3.0.0",],
    entry_points={
        'flake8.report': [
                'junit = flake8reports:Flake8junit',
                'xml = flake8reports:Flake8xml',
                'csv = flake8reports:Flake8csv',
                'tsv = flake8reports:Flake8tsv',
                'ssv = flake8reports:Flake8ssv',
                'json = flake8reports:Flake8json',
            ],
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
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