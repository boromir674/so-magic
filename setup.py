import os
import re
import sys
from setuptools import setup
import subprocess
from collections import OrderedDict


my_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
project_slug = 'so-magic'
setup_cfg_filename = 'setup.cfg'
readme_filename = 'README.rst'
changelog_filename = 'CHANGELOG.rst'
source_code_repo = f'https://github.com/boromir674/{project_slug}'
changelog = f'{source_code_repo}/blob/dev/CHANGELOG.rst'

README = os.path.join(my_dir, readme_filename)

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


def run(cmd):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
    _stdout, _stderr = proc.communicate()

    return proc.returncode, _stdout, _stderr

exit_code, stdout, stderr = run([sys.executable, os.path.join(my_dir, 'scripts', 'parse_package_version.py')])
if exit_code == 0:
    _version = stdout.decode('utf-8').replace('\n', '')
    print(f'Parsed version: {_version}')
else:
    print(stdout)
    print('Failed to automatically parse the package version. Either set it manually in setup.py (or stup.cfg) or'
          'fix the automation.')
    sys.exit(1)

setup(
    version=_version,
    description='library',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    test_suite='tests',
    install_requires=['attrs', 'numpy', 'scikit-learn', 'pandas', 'somoclu'],
    project_urls=OrderedDict([
        ('1-Tracker', f'{source_code_repo}/issues'),
        ('2-Changelog', changelog),
        ('3-Source', source_code_repo),
        ('4-Documentation', f'https://{project_slug}.readthedocs.io/en/dev/'), # "https://blahblah.readthedocs.io/en/v{}/".format(_version)
    ]),

    # download_url='https://github.com/boromir674/music-album-creator/archive/v{}.tar.gz'.format(_version),  # help easy_install do its tricks
    # extras_require={},
    # setup_requires=[],
)
# py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
