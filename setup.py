import os
import re
from setuptools import setup

my_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
SETUP_CFG = 'setup.cfg'
source_code_repo = 'https://github.com/boromir674/so-magic'
# changelog = '{}/blob/master/CHANGELOG.rst'.format(source_code_repo)


def readme():
    with open(os.path.join(my_dir, 'README.rst')) as f:
        return f.read()


def requirements():
    with open(os.path.join(my_dir, 'requirements', 'base.txt')) as fh:
        return fh.read().split('\n')


# Automatically compute package vesion from the [semantic_release] section in setup.cfg
with open(os.path.join(my_dir, SETUP_CFG), 'r') as f:
    regex = r"\[semantic_release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*([\w\.]+(?:/[\w\.]+)*):(\w+)"
    m = re.search(regex, f.read(), re.MULTILINE)
    if m:
        target_file = os.path.join(my_dir, m.group(1))
        target_string = m.group(2)
    else:
        raise RuntimeError(f"Expected to find the '[semantic_release]' section, in the '{SETUP_CFG}' file, with key 'version_variable'."
                           f"\nExaple (it does not have to be a .py file) to idicate that the version is stored in the '__version__' string:\n[semantic_release]\nversion_variable = src/package_name/__init__.py:__version__")


if not os.path.isfile(target_file):
    raise FileNotFoundError(
        f"Path '{target_file} does not appear to be valid. Please go to the '{SETUP_CFG}' file, [semantic_release] section, 'version_variable' key and indicate a valid path (to look for the version string)")

reg_string = r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'

with open(os.path.join(my_dir, target_file), 'r') as f:
    content = f.read()
    reg = f'^{target_string}' + reg_string
    m = re.search(reg, content, re.MULTILINE)
    if m:
        _version = m.group(1)
    else:
        raise AttributeError(f"Could not find a match for regex {reg} when applied to:\n{content}")
###

setup(
    version=_version,
    description='library',
    long_description="TODO long description",
    long_description_content_type='text/x-rst',
    test_suite='tests',
    install_requires=['attrs', 'numpy', 'scikit-learn', 'pandas', 'somoclu'],
    # project_urls=OrderedDict([
    #     # ("1-Tracker", "https://github.com/blahblah/gavgav/issues"),
    #     ("1-Changelog", changelog),
    #     ("2-Source", source_code_repo),
    #     # ("4-Documentation", "https://blahblah.readthedocs.io/en/v{}/".format(_version)),
    # ]),

    # download_url='https://github.com/boromir674/music-album-creator/archive/v{}.tar.gz'.format(_version),  # help easy_install do its tricks
    # extras_require={},
    # setup_requires=[],
)
# py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
