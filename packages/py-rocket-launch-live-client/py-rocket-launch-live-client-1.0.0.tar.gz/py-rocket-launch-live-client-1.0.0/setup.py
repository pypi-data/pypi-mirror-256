import re

import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

# Inspiration: https://stackoverflow.com/a/7071358/6064135
with open('py_rocket_launch_live_client/_version.py', 'r') as version_file:
    version_groups = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_groups:
        version = version_groups.group(1)
    else:
        raise RuntimeError('Unable to find version string!')

REQUIREMENTS = [
    'pandas',
    'requests'
    # Add your list of production dependencies here, eg:
    # 'requests == 2.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.7.*',
    'black == 23.*',
    'build == 0.10.*',
    'flake8 == 6.*',
    'isort == 5.*',
    'mypy == 1.5.*',
    'pytest == 7.*',
    'pytest-cov == 4.*',
    'twine == 4.*',
]

setuptools.setup(
    name='py-rocket-launch-live-client',
    version=version,
    description='Python Client for RocketLaunchLive API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/arthur-clifford/py-rocket-lauch-live-client',
    author='arthur-clifford',
    author_email='artclifford@me.com',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=[
            'examples',
            'test',
        ]
    ),
    package_data={
        'py_rocket_launch_live_client': [
            'py.typed',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'py-rocket-lauch-live-client=py_rocket_lauch_live_client.module:main',
        ]
    },
    python_requires='>=3.10, <4',
)
