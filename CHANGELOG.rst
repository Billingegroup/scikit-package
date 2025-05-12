=============
Release notes
=============

.. current developments

0.0.2
=====

**Changed:**

* Provide separate documentation instructions for starting a new project vs. migrating an existing package.


0.0.1
=====

**Added:**

* Add full description of ``scikit-package`` in ``pyproject.toml``.
* Add motivating statements under the Statement of need section in ``index.rst``.
* Add ``package create`` and ``package update`` commands once ``scikit-package`` is installed.
* Add instructions on pre-commit GitHub setup, how to test package and render doc locally
* Add FAQ descriptions on Github workflow, namespace package setup, deploy docs via GitHub Actions
* Add extra metadata of email, name, username, license holder, etc. collected to dynamically populate rendered cookiecuttered files.
* Add conda-forge feedstock creation and maintenance guide.
* Add instructions for Codecov setup in documentation.
* Add FAQ section to the documentation on how to customize the template and design decisions for the current setup.
* Add demo .gif file used in README.rst in generating a package and building documentation with ``scikit-package``.
* Add ``Getting started`` page in documentation.
* Add FAQ section on why both ``pip.txt```` and ``conda.txt`` added.
* Add FAQ section on how version is set and retrieved dynamically.
* Support Billinge group's reusesable workflow by adding requirement files and ``environment.yml``.
* Add Sphinx documentation for ``scikit-package``.
* Add documentation for Python package release with GitHub Actions.
* Use field-list feature in Sphinx to better manage the user inputs in How to cookiecut package section
* Add automatic linting of .md, .yml, .rst files via prettier hook in ``pre-commit``.
* Add automatic docstring linting with PEP 257 compliance with ``docformatter`` in ``pre-commit``.
* Configure ``PYTHON_MAX_VERSION`` and ``PYTHON_MIN_VERSION`` in ``doc/source/conf.py`` to increase maintainability throughout the documentation.

**Changed:**

* Rename repositroy and package name to ``scikit-package``.
* Import ``package_dir_name```` in the ``__init__.py`` instead of ``conda_pypi_package_dist_name`` to ensure package import is lowercased.
* Change default line-length to 79 characters in ``black``, ``flake``, and ``isort`` configuration files for PEP8 compatibility.
* Change question and default answer format on user prompt on C extension and headless GUI with improved wording.
* Standarlize the current repository based on ``scikit-package`` structure.

**Fixed:**

* Update corresponding email to sb2896@columbia.edu.
