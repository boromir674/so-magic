***************
Installation
***************

| So Magic was desinged with the intention to be pip installable. Unfortunately,
| even though $pip install so-magic$ will install the library from the pypi (index) server,
| it is possible that the somoclu library (which is a dependency) will be missing a critical feature.

| If you have successfully (build and) installed somoclu in your environment
| then you can indeed install so-magic from pypi.

| Example command:

.. code-block::

    pip install so-magic

See the `somoclu documentation`_ pages to read more about the library features.


Linux & macOS
=============
Unfortunately, it is possible that none of the two official `installation methods`_ for
somoclu would work as expected. Namely the method of invoking :code:`pip install somoclu` and the
method of building somoclu from source.

It has been documented (see :issue:`136`), and verified by the author on a macOS Catalina, that you might run into
an issue with clang and OpenMP that breaks the build process.
It is also possible that installation succeeds, but when your client code invokes the
"wrap_train" function, a NameError exception (see :issue:`28`) is thrown on the Python side.

Thus, it is recommended that you install so-magic using anaconda.
Anaconda succeeds in doing conda install somoclu in contrast to pip

Prepare a conda environment (just like a virtualenv):

.. code-block:: shell

    ENV_PATH=so-magic-env
    conda create -p $ENV_PATH -y python=3.7
    FILE_TO_SOURCE="$HOME/miniconda/etc/profile.d/conda.sh"
    if [[ ! -f $FILE_TO_SOURCE ]]; then
      source "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
      source "$HOME/miniconda/etc/profile.d/conda.sh"
    fi
    hash -r
    conda config --set always_yes yes --set changeps1 no
    conda update -q conda
    conda info -a
    conda activate $ENV_PATH

Install somoclu dependency:

.. code-block:: shell

    conda install somoclu --channel conda-forge

Install latest so-magic:

.. code-block:: shell

    pip install so-magic



.. _SO: https://stackoverflow.com/

.. _somoclu documentation: https://somoclu.readthedocs.io/en/stable/

.. _installation methods: https://somoclu.readthedocs.io/en/stable/download.html
