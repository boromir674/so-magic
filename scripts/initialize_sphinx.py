import os
import re

# CONSTANSTS
my_dir = os.path.dirname(os.path.realpath(__file__))
REPO_ROOT = os.path.join(my_dir, '..')
CONF_PY = os.path.join(REPO_ROOT, 'docs', 'conf.py')

## CONFIG
# 1. Automatic extensions registration
EXTENSIONS = [
    'sphinx.ext.doctest',  # to support doctest builder
    'sphinx.ext.autodoc',  # to support extracting documentation from docstrings supporting default format rst (javadoc-like)
    'sphinx.ext.napoleon',  # enable support for google and numpy format for autodoc
]
# 2. Automatic parsing of software release version
CONFIG_INI = os.path.join(REPO_ROOT, 'setup.cfg')
SECTION = 'semantic_release'
FIELD = 'version_variable'
# 3. Automatic updating $PATH to enable working with autodoc
PATHS = [
    'src/so_magic',
]
DEPS = ['os', 'sys']

## SCRIPT
def set_extensions(string, extensions):
    """Register sphinx extensions by populating the 'extentions' list."""
    return re.sub('(extensions[ \t]*=[ \t\n]*\[\n*)(.*\n*\])', "\\1" +  ',\n'.join(f"'{x}'" for x in extensions) + ",\n\\2", string)


def set_release(string, version_string):
    """Register the release version in the X.Y.Z. For example 0.5.0 (not v0.5.0)."""
    return re.sub('(release[ \t]*=[ \t])(.*)', "\\1'" + version_string + "'", string)


# Automatically compute package vesion from the [semantic_release] section in setup.cfg
def get_version_string(config_file, section, field):
    """Read the software release version as a string with format xX.Y.Z ie v0.1.0"""
    with open(os.path.join(config_file), 'r') as f:
        regex = r"\[semantic_release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*([\w\.]+(?:/[\w\.]+)*):(\w+)"
        m = re.search(regex, f.read(), re.MULTILINE)
        if m:
            target_file = os.path.join(REPO_ROOT, m.group(1))
            target_string = m.group(2)
        else:
            raise RuntimeError(
                f"Expected to find the '[semantic_release]' section, in the '{config_file}' file, with key 'version_variable'."
                f"\nExaple (it does not have to be a .py file) to idicate that the version is stored in the '__version__' string:\n[semantic_release]\nversion_variable = src/package_name/__init__.py:__version__")

    if not os.path.isfile(target_file):
        raise FileNotFoundError(
            f"Path '{target_file} does not appear to be valid. Please go to the '{config_file}' file, [semantic_release] section, 'version_variable' key and indicate a valid path to a file that contains the version string")

    reg_string = r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'

    with open(os.path.join(target_file), 'r') as f:
        content = f.read()
        reg = f'^{target_string}' + reg_string
        m = re.search(reg, content, re.MULTILINE)
        if m:
            _version = m.group(1)
        else:
            raise AttributeError(f"Could not find a match for regex {reg} when applied to:\n{content}")
    return _version

def set_to_sys_path(string, paths, libs):
    """Each path is relative to the repo root folder.

    Add extensions (or modules to document with autodoc) that are in another directory,
    add these directories to sys.path here. If the directory is relative to the
    documentation root, use os.path.abspath to make it absolute, like shown here.
    """
    def search(a_line):
        for lib_name in libs:
            if re.match('import {lib}'.format(lib=lib_name), a_line):
                libs.remove(lib_name)
                break
    lines = string.split('\n')
    i = 0
    exist_lines_to_traverse = i < len(lines)
    exist_dependencies_to_satisfy = bool(libs)
    while exist_lines_to_traverse and exist_dependencies_to_satisfy:
        search(lines[i])
        i += 1
    path_update_lines = [f"sys.path.insert(0, os.path.abspath('../{relative_path}'))" for relative_path in paths]
    if i == len(lines): # did not find import statements, so we do a manual fix here by including them in the file
        new_lines = [f'import {lib}' for lib in libs] + path_update_lines + lines
    else:
        new_lines = lines[:i] + path_update_lines + lines[i:]
    return '\n'.join(new_lines)


def import_lib(string, lib_name):
    """Add an import statement on top of the file."""
    return f'import {lib_name}\n{string}'

def uncomment_import(string, lib_name):
    """"""
    return re.sub(r'#[\t ]*(import {lib})'.format(lib=lib_name), "\\1", string)


def main():
    # read input file
    fin = open(CONF_PY, "rt")
    data = fin.read()

    # 1. Automatically register extentions
    data = set_extensions(data, EXTENSIONS)

    # 2. Automatically set the 'release' variable based on semantic_release (see setup.cfg)
    try:
        version = get_version_string(CONFIG_INI, SECTION, FIELD)
        data = set_release(data, version.replace('v', ''))
    except (RuntimeError, FileNotFoundError, AttributeError) as e:
        print(e)
        print("<<Please set the 'release' variable in conf.py manually.>>")

    # 3. Automatically update $PATH to support using autodoc extention
    for lib in DEPS:
        data = uncomment_import(data, lib)
    data = set_to_sys_path(data, PATHS, DEPS)

    fin.close()
    fin = open(CONF_PY, "wt")
    # overrite the input file with the resulting data
    fin.write(data)
    fin.close()


if __name__ == '__main__':
    main()
