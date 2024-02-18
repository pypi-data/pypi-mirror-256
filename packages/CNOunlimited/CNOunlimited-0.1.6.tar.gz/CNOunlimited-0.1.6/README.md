# CNOunlimited
Python Package repository for code that we have to commonly re-use in our automations and observability engineering.

## Installation

To install the package, run 'pip install CNOunlimited'


## Committing changes to the package

After making changes, commit the code to github with 'git add .' and 'git commit -m "message"'

Then push the code to github with 'git push'

Update the version in setup.py

Then, to update the package on pypi, run 'python setup.py sdist bdist_wheel' to create the package files.

Then, run 'twine upload dist/*' to upload the package to pypi.