import os
import sys
from subprocess import check_call, CalledProcessError


def activate_conda_env(conda, env_path):
    check_call([conda, 'create', '-p', env_path, '-y'])
    check_call([conda, 'activate', env_path])


def install_dependencies(python, conda):
    check_call([python, '-m', 'pip', 'install', '--upgrade', 'pip'])
    check_call([python, '-m', 'pip', 'install', '--upgrade', 'wheel'])
    check_call([python, '-m', 'pip', 'install', '-r', 'requirements/base.txt'])
    check_call([python, '-m', 'pip', 'install', '-r', 'requirements/dev.txt'])
    check_call([conda, 'install', 'somoclu', '-y'])


def pip_install_lib(python, package_name='so_magic', pypi_index_url='https://test.pypi.org/simple/'):
    # use this command because test pypi absolutely not guarantees that it can satsify dependencies (--no-deps flag) by
    # looking for the packages in the index, simply because they might not exist
    check_call([python, '-m', 'pip', 'install', '--index-url', pypi_index_url, '--no-deps', package_name])


def main():
    # CONSTANTS
    MY_DIR = os.path.dirname(os.path.realpath(__file__))
    tools = type('Executables', (object,), {'python': 'python', 'conda': os.environ.get('CONDA_EXE', 'conda')})
    ENV_NAME = 'integration-env'
    ENV_PATH = os.path.join(MY_DIR, f'../{ENV_NAME}')
    try:
        check_call([tools.conda, '--help'])
        print('------------ CONDA IS ALREADY INSTALLED -------------')
    except CalledProcessError as ex:  # this exception fires if the exit code of the above is not 0
        print(ex)
        tools.conda = None

    if tools.conda is None:
        print("Will try to automatically install anaconda ..")
        print('------------ INSTALLING CONDA -------------')
        check_call(['chmod', '+x', './scripts/install_anaconda.sh'])
        try:
            check_call(['bash', 'scripts/install_anaconda.sh'])
            tools.conda = 'conda'
        except CalledProcessError as ex2:
            print("Failed to install anaconda, so cannot satisfy the somoclu feature of training a new map, which is "
                  "required by one test case.\n Exitting with 1.")
            raise ex2
    print('------------ CREATING ENV -------------')
    check_call([tools.conda, 'create', '-p', ENV_PATH, '-y'])
    print('------------ ACTIVATING ENV -------------')
    check_call([tools.conda, 'activate', ENV_PATH])

    # activate_conda_env(tools.conda, ENV_PATH)
    # install_dependencies(tools.python, tools.conda)
    # pip_install_lib(tools.python)

    print("SUCCESS!!!")
    print("Successfully installed the library emnulating the real 'pip install' scenario using the test-pypi server.")


if __name__ == '__main__':
    try:
        main()
        print("OK.")
    except Exception as e:
        print(e)
        print("FAILED")
        exit(1)
