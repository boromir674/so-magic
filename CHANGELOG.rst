0.6.0 (2021-05-30)
------------------

feature
"""""""
- allow both method & classmethod as client implementation of TabularData operations

test
""""
- make unit-tests code coverage 100% when running the test suite
- automate tabular operators tests
- assert all tabular data operations implementations follow interfaces


0.5.3 (2021-05-25)
------------------

documentation
"""""""""""""
- redesign the README.rst


0.5.2 (2021-05-22)
------------------

documentation
"""""""""""""
- report correct code coverage and other values of code badges

ci
""
- add the .prospector.yml configuration file and avoid crash (due to .pylintrc)


0.5.1 (2021-04-22)
-------------------

feature
"""""""
- add __name__ & __doc__ attributes to newly registered phis created out of class
- automatically discover the commands definitions and build prototype commands

test
""""
- assert that instantiation from Observer is not allowed, since it is an interface

documentation
"""""""""""""
- re-design utils package api rtd documentation
- fix warnings of phi module and test the example code by running it in a doctest session
- document the purpose of the backend module (defines data_engine_wrapper)
- fix word spelling, eliminate docs build command warnings
- document the purpose of the phi.py module, being to officially register new phi functions
- document purpose of magic_datapoints_factory and the Interfaces related to table-like data
- document the purpose of the TabularDataInterface
- document the purpose of the DatapointsManager class
- add 'quickstart' section and restructure utils

ci
""
- split check, build & deploy tox envs, add uml command to circleci, add pyroma check to all CIs
- define an environment to generate uml (class & package) diagrams by inspecting the code
- speed up jobs and revamp pipeline
- remove the windows ci pipeline running on appveyor
- pass the .git directory to the send-test-to-codecov job
- define job to send coverage to codecov.io and run it on every commit
- add the --cov and --cov-report=term-missing cli arguments to the dev-cov command
- document the 'graphs' env that creates visualization(s) of the Python dependencies
- manually install the py package before trasforming the test results into html & xml
- add 2 tox test envs that run tests against the code by using a development setup
- inform where to find the built html-based documentation index.html


0.4.4 (2019-11-16)
------------------
- minor fix

0.4.3 (2019-11-16)
------------------
- minor fix

0.4.1 (2019-11-15)
------------------

- minor fixes

0.4.0 (2019-11-15)
------------------

Changes
^^^^^^^

feature
"""""""
- library documentation on https://so-magic.readthedocs.io/
- write installation guide for Linux & macOS

documentation
"""""""""""""
- add introduction, installation and API reference (with autodoc & sphinx-apidoc)

ci
""
- add configuration for automatically building and hosting the documentation on readthedocs.org


0.3.16 (2019-11-13)
-------------------

Changes
^^^^^^^

ci
""
- travis-ci.org jobs: fix 'deploy-to-staging' & optimize 'documention-building' related jobs


0.3.15 (2019-11-12)
-------------------

Changes
^^^^^^^

documentation
"""""""""""""
- point badge to correct branch


0.3.14 (2019-11-12)
-------------------

Changes
^^^^^^^

test
""""
- automated integration test involving the staging server

ci
""
- Continuous Integration & Continuous Deployment on CircleCI server


0.3.0 (2019-11-03)
------------------
Changes
^^^^^^^

feature
"""""""
- add the ability to perform linear transformations
- allow registering arbitrary functions as commands
- send code coverage data to codacy

documentation
"""""""""""""
- point docs badge to dev branch of remote
- enable doctest extension and add spelling as dependency
- pass quickstart and spelling task

ci
""
- do not report assert statements "errors" to avoid false positives found in unit-test code
- autoprovision tox-conda to install somoclu dependency and wrap the train function
