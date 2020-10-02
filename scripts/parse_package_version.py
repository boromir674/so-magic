import os
import re
import sys

my_dir = os.path.dirname(os.path.realpath(__file__))

setup_cfg_filename = 'setup.cfg'
SETUP_CFG = os.path.join(my_dir, '../', setup_cfg_filename)


def main():
    """Get the package version string provided that the developer has setup indication how to find it."""
    # Automatically compute package vesion from the [semantic_release] section in setup.cfg
    with open(SETUP_CFG, 'r') as f:
        regex = r"\[semantic_release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*([\w\.]+(?:/[\w\.]+)*):(\w+)"
        m = re.search(regex, f.read(), re.MULTILINE)
        if m:
            file_with_version_string = os.path.join(my_dir, '../', m.group(1))
            variable_holding_version_value = m.group(2)
        else:
            raise RuntimeError(
                f"Expected to find the '[semantic_release]' section, in the '{SETUP_CFG}' file, with key 'version_variable'."
                f"\nExample (it does not have to be a .py file) to indicate that the version is stored in the '__version__' string:\n[semantic_release]\nversion_variable = src/package_name/__init__.py:__version__")

    if not os.path.isfile(file_with_version_string):
        raise FileNotFoundError(
            f"Path '{file_with_version_string} does not appear to be valid. Please go to the '{SETUP_CFG}' file, at the [semantic_release] section and set the 'version_variable' key with a valid path (to look for the version string)")

    reg_string = r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'

    with open(file_with_version_string, 'r') as f:
        content = f.read()
        reg = f'^{variable_holding_version_value}' + reg_string
        m = re.search(reg, content, re.MULTILINE)
        if m:
            _version = m.group(1)
            return _version
        else:
            raise AttributeError(f"Could not find a match for regex {reg} when applied to:\n{content}")


if __name__ == '__main__':
    try:
        version_string = main()
        print(version_string)
    except (RuntimeError, FileNotFoundError, AttributeError) as e:
        print(e)
        sys.exit(1)
