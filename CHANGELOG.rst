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
