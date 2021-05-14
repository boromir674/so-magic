import os
import sys
from setuptools import setup
import subprocess
from collections import OrderedDict


my_dir = os.path.dirname(os.path.realpath(__file__))


# Modify based on your project
project_slug = 'so-magic'
changelog_filename = 'CHANGELOG.rst'
source_code_repo = f'https://github.com/boromir674/{project_slug}'
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
    _version = stdout.decode('utf-8').replace('\n', '')
    print(f'Parsed version: {_version}')
else:
    print(stdout)
    print('Failed to automatically parse the package version. Either set it manually in setup.py (or stup.cfg) or'
          'fix the automation.')
    sys.exit(1)

setup(
    name=project_slug,
    version=_version,
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
        ('Documentation', f'https://{project_slug}.readthedocs.io/'), # "https://blahblah.readthedocs.io/en/v{}/".format(_version)
    ]),
    download_url=f'https://github.com/boromir674/so-magic/archive/v{_version}.tar.gz',  # help easy_install do its tricks
    # extras_require={},
    # setup_requires=[],
)
# py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
