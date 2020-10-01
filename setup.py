import os
import re
from setuptools import setup
from collections import OrderedDict


my_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
setup_cfg_filename = 'setup.cfg'
readme_filename = 'README.rst'
changelog_filename = 'CHANGELOG.rst'
source_code_repo = 'https://github.com/boromir674/so-magic'
# changelog = '{}/blob/master/CHANGELOG.rst'.format(source_code_repo)

README = os.path.join(my_dir, readme_filename)
CHANGELOG = os.path.join(my_dir, changelog_filename)

# Compute long description that will be rendered in the pypi server
long_description = ''
if not long_description:  # if not custom long description is supplied, then create one automatically
    if not os.path.isfile(README):
        long_description = 'Pending to provide with a long description for the software/package'
    else:
        with open(README) as f:
            long_description = f.read()


def requirements():
    with open(os.path.join(my_dir, 'requirements', 'base.txt')) as fh:
        return fh.read().split('\n')


# Automatically compute package vesion from the [semantic_release] section in setup.cfg
with open(os.path.join(my_dir, setup_cfg_filename), 'r') as f:
    regex = r"\[semantic_release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*([\w\.]+(?:/[\w\.]+)*):(\w+)"
    m = re.search(regex, f.read(), re.MULTILINE)
    if m:
        target_file = os.path.join(my_dir, m.group(1))
        target_string = m.group(2)
    else:
        raise RuntimeError(f"Expected to find the '[semantic_release]' section, in the '{setup_cfg_filename}' file, with key 'version_variable'."
                           f"\nExample (it does not have to be a .py file) to indicate that the version is stored in the '__version__' string:\n[semantic_release]\nversion_variable = src/package_name/__init__.py:__version__")


if not os.path.isfile(target_file):
    raise FileNotFoundError(
        f"Path '{target_file} does not appear to be valid. Please go to the '{setup_cfg_filename}' file, [semantic_release] section, 'version_variable' key and indicate a valid path (to look for the version string)")

reg_string = r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'

with open(os.path.join(my_dir, target_file), 'r') as f:
    content = f.read()
    reg = f'^{target_string}' + reg_string
    m = re.search(reg, content, re.MULTILINE)
    if m:
        _version = m.group(1)
    else:
        raise AttributeError(f"Could not find a match for regex {reg} when applied to:\n{content}")


setup(
    version=_version,
    description='library',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    test_suite='tests',
    install_requires=['attrs', 'numpy', 'scikit-learn', 'pandas', 'somoclu'],
    project_urls=OrderedDict([
        ('1-Tracker', f'{source_code_repo}/issues'),
        ('2-Changelog', CHANGELOG),
        ('3-Source', source_code_repo),
        ('4-Documentation', 'https://so-magic.readthedocs.io/en/dev/'), # "https://blahblah.readthedocs.io/en/v{}/".format(_version)
    ]),

    # download_url='https://github.com/boromir674/music-album-creator/archive/v{}.tar.gz'.format(_version),  # help easy_install do its tricks
    # extras_require={},
    # setup_requires=[],
)
# py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
