import os
import sys
import subprocess
from collections import OrderedDict
from setuptools import setup


my_dir = os.path.dirname(os.path.realpath(__file__))


# Modify based on your project
PROJECT_SLUG = 'so-magic'
CHANGELOG_FILENAME = 'CHANGELOG.rst'
source_code_repo = f'https://github.com/boromir674/{PROJECT_SLUG}'
changelog = f'{source_code_repo}/blob/master/CHANGELOG.rst'


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
    VERSION = stdout.decode('utf-8').replace('\n', '')
    print(f'Parsed version: {VERSION}')
else:
    print(stdout)
    print('Failed to automatically parse the package version. Either set it manually in setup.py (or setup.cfg) or'
          'fix the automation.')
    sys.exit(1)

setup(
    name=PROJECT_SLUG,
    version=VERSION,
    long_description_content_type='text/x-rst',
    author='Konstantinos Lampridis',
    author_email='k.lampridis@hotmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    project_urls=OrderedDict([
        ('Issue Tracker', f'{source_code_repo}/issues'),
        ('Changelog', changelog),
        ('Source', source_code_repo),
        ('Documentation', f'https://{PROJECT_SLUG}.readthedocs.io/'),
    ]),
    download_url=f'https://github.com/boromir674/so-magic/archive/v{VERSION}.tar.gz',  # help easy_install do its tricks
)
