# CNOunlimited
Python Package repository for code that we have to commonly re-use in our automations and observability engineering.

## Installation

To install the package, run 'pip install CNOunlimited'


## Committing changes to the package

Update the version in setup.py

After making changes, commit the code to github with 'git add .' and 'git commit -m "message"'

Then push the code to github with 'git push'

Then, to update the package on pypi, run 'python setup.py sdist bdist_wheel' to create the package files.

Then, run 'twine upload dist/*' to upload the package to pypi.
    Your username for this will be __token__ and the password is stored in secrets.ini