"""
AppVeyor will at least have few Pythons around so there's no point of implementing a bootstrapper in PowerShell.

This is a port of https://github.com/pypa/python-packaging-user-guide/blob/master/source/code/install.ps1
with various fixes and improvements that just weren't feasible to implement in PowerShell.
"""
from __future__ import print_function

from os import environ
from os.path import exists
from subprocess import check_call

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

BASE_URL = "https://www.python.org/ftp/python/"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
GET_PIP_PATH = "C:\get-pip.py"
URLS = {
    ("2.7", "64"): BASE_URL + "2.7.13/python-2.7.13.amd64.msi",
    ("2.7", "32"): BASE_URL + "2.7.13/python-2.7.13.msi",
    ("3.4", "64"): BASE_URL + "3.4.4/python-3.4.4.amd64.msi",
    ("3.4", "32"): BASE_URL + "3.4.4/python-3.4.4.msi",
    ("3.5", "64"): BASE_URL + "3.5.4/python-3.5.4-amd64.exe",
    ("3.5", "32"): BASE_URL + "3.5.4/python-3.5.4.exe",
    ("3.6", "64"): BASE_URL + "3.6.2/python-3.6.2-amd64.exe",
    ("3.6", "32"): BASE_URL + "3.6.2/python-3.6.2.exe",
    ("3.7", "32"): BASE_URL + "3.7.8/python-3.7.8-amd64.exe",
    ("3.7", "64"): BASE_URL + "3.7.8/python-3.7.8.exe",
    ("3.8", "32"): BASE_URL + "3.8.4/python-3.8.4-amd64.exe",
    ("3.8", "64"): BASE_URL + "3.8.4/python-3.8.4.exe",
}
INSTALL_CMD = {
    # Commands are allowed to fail only if they are not the last command.  Eg: uninstall (/x) allowed to fail.
    "2.7": [["msiexec.exe", "/L*+!", "install.log", "/qn", "/x", "{path}"],
            ["msiexec.exe", "/L*+!", "install.log", "/qn", "/i", "{path}", "TARGETDIR={home}"]],
    "3.4": [["msiexec.exe", "/L*+!", "install.log", "/qn", "/x", "{path}"],
            ["msiexec.exe", "/L*+!", "install.log", "/qn", "/i", "{path}", "TARGETDIR={home}"]],
    "3.5": [["{path}", "/quiet", "TargetDir={home}"]],
    "3.6": [["{path}", "/quiet", "TargetDir={home}"]],
    "3.7": [["{path}", "/quiet", "TargetDir={home}"]],
    "3.8": [["{path}", "/quiet", "TargetDir={home}"]],
}

def command_iterator(version, **kwargs):
    """Call to iterate through the defined commands, given a python version. Each command is a list of words"""
    return iter([part.format(home=kwargs['home'], path=kwargs['path']) for part in cmd] for cmd in INSTALL_CMD[version])


def exec_command(cmd):
    print("Running:", " ".join(cmd))
    try:
        check_call(cmd)
        return True
    except Exception as e:
        print("Failed command", cmd, "with:", e)
        if exists("install.log"):
            with open("install.log") as f:
                print(f.read())
        return False

def download_file(url, path):
    print("Downloading: {} (into {})".format(url, path))
    progress = [0, 0]

    def report(count, size, total):
        progress[0] = count * size
        if progress[0] - progress[1] > 1000000:
            progress[1] = progress[0]
            print("Downloaded {:,}/{:,} ...".format(progress[1], total))

    dest, _ = urlretrieve(url, path, reporthook=report)
    return dest


def install_python(python_specs):
    print("Installing Python", python_specs.version, "for", python_specs.arch, "bit architecture to", python_specs.home)
    if exists(python_specs.home):
        return
    path = download_python(python_specs.version, python_specs.arch)
    print("Installing", python_specs.path, "to", python_specs.home)
    success = any(x == True for x in [exec_command(cmd) for cmd in command_iterator(version, home=python_specs.home, path=python_specs.path)])
    if success:
        print("Installation complete!")
    else:
        print("Installation failed")


def download_python(version, arch):
    for _ in range(3):
        try:
            return download_file(URLS[version, arch], "installer.exe")
        except Exception as exc:
            print("Failed to download:", exc)
        print("Retrying ...")


def install_pip(home):
    pip_path = home + "/Scripts/pip.exe"
    python_path = home + "/python.exe"
    if exists(pip_path):
        print("pip already installed.")
    else:
        print("Installing pip...")
        download_file(GET_PIP_URL, GET_PIP_PATH)
        print("Executing:", python_path, GET_PIP_PATH)
        check_call([python_path, GET_PIP_PATH])

def upgrade_pip(python_home_folder):
    print('Upgrading pip ..')
    try:
        check_call([python_home_folder + '/python.exe', '-m', 'pip', 'install', '--upgrade', 'pip'])
    except Exception as e:
        print("Failed to upgade pip: {}".format(e))


def install_packages(home, *packages):
    print('Installing packages [{}]'.format(', '.join(str(_) for _ in packages)))
    # cmd = [home + "/Scripts/pip.exe", "install"]
    cmd = [home + "/python.exe", "-m", "pip", "install"]
    cmd.extend(packages)
    check_call(cmd)


if __name__ == "__main__":
    python_specs = type('PythonSpecs', (object,), {'version': environ['PYTHON_VERSION'],
                                                   'arch': environ['PYTHON_ARCH'],
                                                   'home': environ['PYTHON_HOME']})
    install_python(python_specs)
    install_pip(environ['PYTHON_HOME'])
    upgrade_pip(environ['PYTHON_HOME'])
    install_packages(environ['PYTHON_HOME'], "setuptools>=40.0.0", "wheel", "tox", "virtualenv>=20.0.0")
