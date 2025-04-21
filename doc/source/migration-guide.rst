:tocdepth: -1

.. index:: migration-guide

.. _migration-guide:

==============================================================
Migrate your existing package with ``scikit-package``
==============================================================

Prerequisites
-------------

This guide is for developers who have an existing Python package and want to migrate it to the Billinge group's project structure using the ``scikit-package`` library up to Level 5.

Hence, we assume you have a basic understanding of Python, Git, and GitHub workflows, and ``pre-commit`` and ``pytest``. If you are not familiar with GitHub workflows, please refer our brief guide provided :ref:`here <github-workflow-overview>`.

We also assume you have already used ``scikit-package`` at least up to the Level 4 level and also at least have read through the guide provided for Level 5.

Tips and how to receive support
-------------------------------

We understand that your migration journey can be challenging. We offer the following ways to help guide migrate your package to scikit-package:

#. You may cross-check with the Billinge group's up-to-date package, ``diffpy.utils``: https://github.com/diffpy/diffpy.utils.

#. If you have any questions, first read the :ref:`FAQ <frequently-asked-questions>` for how to customize your package and certain design decisions in the scikit-package template.

#. After you've cross-checked and searched through the FAQ, please feel free to ask questions by creating an issue on the scikit-package repository `here <https://github.com/Billingegroup/scikit-package/issues>`_.

Migration overview and expected outcome
---------------------------------------

By the end of the migration process, you will have a package that is structured according to the Billinge group's project structure shown here: https://github.com/diffpy/diffpy.utils. The migration process is divided into four main steps.

#. During the first step of the :ref:`pre-commit workflow <migration-pre-commit>`, you will use automatic formatting tools to standardize your package with PEP8 before migrating it to the Billinge group's project structure with ``scikit-package``.

#. In the :ref:`migration workflow  <migration-workflow>`, you will use the ``scikit-package`` library to generate a new project inside the original directory. The new project contains dynamically filled templates based on your package information, and configure GitHub CI and Codecov.

#. In the :ref:`API documentation build workflow <scikit-package-workflow-doc>`, you will use our Python script to automatically generate and build API documentation for your package and render the documentation locally.

#. In the final :ref:`clean-up workflow <scikit-package-workflow-cleanup>`, you will host your package documentation online. Your package will be in good shape for PyPI, GitHub, and conda-forge release!

.. _migration-pre-commit:

.. include:: snippets/scikit-installation.rst

1. Pre-commit workflow
----------------------

Here, let's first standarlize your package so that itis ``PEP8`` and ``PEP256`` compliant using both automatic formatting tools with manual edits.

1.1. Run black in your codebase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Fork the repository that you want to standarlize from the GitHub website under your GitHub account.

    If you are the owner of the repository, you can skip this step.

#. Type ``git clone <https://github.com/<username>/<project-name>`` and ``cd <project-name>``.

#. Type ``git pull upstream main`` to sync with the ``main`` branch.

    If your default branch is called ``master``, run ``git pull upstream master`` instead. However, ``main`` is the new default branch name for GitHub.

#. Type ``pip install black`` to install ``black``.

#. Type ``git checkout -b black`` to create a new branch called ``black``.

#. Create ``pyproject.toml`` at the top project level.

#. Copy and paste with the following content to ``pyproject.toml``:

    .. code-block::

        [tool.black]
        line-length = 79
        include = '\.pyi?$'
         exclude = '''
         /(
             \.git
         | \.hg
         | \.mypy_cache
         | \.tox
         | \.venv
         | \.rst
         | \.txt
         | _build
         | buck-out
         | build
         | dist
         # The following are specific to Black, you probably don't want those.
         | blib2to3
         | tests/data
         )/
         '''

#. Type ``black src``. If your source code is in a different directory, replace ``src`` with the appropriate directory path. This will automatically format given the line-length provided under ``line-length`` above in ``pyproject.toml``. If you want to ignore specific files or directories, add them to the ``exclude`` section in ``pyproject.toml``

#. Add and commit the automatic changes by ``black``. The commit message can be ``git commit -m "skpkg: apply black to src directory with black configured in pyproject.toml"``.

#. Type ``black .`` Here, you are running black across the entire package directory. Run ``pytest`` to test locally.

#. Type ``git add .`` and ``git commit -m "skpkg: apply black to all files in the project directory"``.

#. Create a pull request into ``main``. The pull request title can be ``skpkg: Apply black to project directory with no manual edits``.

#. Wait for the PR to be merged to ``main``.

#. Done. Let's apply ``pre-commit`` hooks to the project directory next.

1.2. Apply pre-commit hooks without manual edits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We will setup ``pre-commit`` locally and also via GitHub CI.

#. Type ``git checkout main && git pull upstream main`` and ``git branch -b pre-commit`` to create a new branch called ``pre-commit``.

#. Copy and paste three files of ``.flake8``, ``.isort.cfg``, ``.pre-commit-config.yaml`` from https://github.com/Billingegroup/scikit-package/tree/main/%7B%7B%20cookiecutter.github_repo_name%20%7D%7D to your project directory.

#. Type ``git add .flake8 .isort.cfg .pre-commit-config.yaml``

#. Type ``pre-commit run --all-files``. It will attempt to lint your code such as docstrings, extra spaces, across all file types such as ``.yml``, ``.md``, ``.rst``, etc.

#. Type ``git status`` to get an overview of the files modified and then by running ``git diff <file-or-directory-path>`` to see the specific changes.

#. If you do not want the new changes, you can run ``git restore <file-or-directory-path>`` to revert the changes done by ``pre-commit``.

#. If you want to prevent ``prettier`` from applying on specific files, create ``.`prettierignore`` file at the top project like shown here: https://github.com/Billingegroup/scikit-package/blob/main/.prettierignore

#. If you are satisfied with the automatic changes by ``pre-commit run --all-files``, run ``pytest``, type ``git add <file-path(s)>`` and ``git commit -m "style: apply pre-commit hooks with no manual edits"``.

    .. Attention:: At this point, you may have failed hooks when you run ``pre-commit run --all-files``. Don't worry! We will fix them in the following section.

#. Push the changes to the ``pre-commit`` branch by typing ``git push origin pre-commit``.

#. Create a PR from ``pre-commit`` to ``package`` branch. The PR title can be ``skpkg: Apply pre-commit to project directory with no manual edits``.

#. Merge the PR to ``package``. CIs will most likely fail, don't worry. We will fix them slowly.

.. _migration-pre-commit-manual-edits:

1.3. Apply manual edits to pass ``pre-commit`` hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your package will most likely have failed pre-commit hooks. We will manually fix the errors raised by ``flake8``, ``codespell``, etc.

#. Type ``git checkout upstream package && git pull upstream package`` to sync with the ``package`` branch.

#. Type ``git checkout -b flake8-length`` to create a new branch. In this branch you will fix flake8 errors. In this branch, fix all of ``flake8`` errors related to line-lenghts if there are any. If you want to ignore certain files from flake8 errors include filepaths to ``exclude`` section in the ``.flake8`` files.

#. Create a PR to ``package``. Since you are fixing flake8 errors, the commit message can be ``skpkg: fix flake8 line-length errors`` and the pull request title can be ``skpkg: Fix flake8 line-length errors``.

#. If you have ``codespell`` errors, create a new branch called ``codespell`` and fix all of the spelling errors. You can ignore specific words or lines by following the instructions provided here in the FAQ section :ref:`here <codespell-ignore>`.

#. If you want to suppress the ``flake8`` error, add ``# noqa: <error-code>`` at the end of the line. For example, ``import numpy as np # noqa: E000`` but make sure you create an issue for this so that you can revisit them.

#. For each `flake8` branch, create a PR request to ``package``. Since you are fixing flake8 errors, the commit message can be ``skpkg: Fix flake8 <readable-error-type> errors`` and the pull request title can be ``skpkg: Fix flake8 <readable-error-type> errors``.

#. For each PR, either the project owner or the maintainer will review the PR and merge it to ``package``. If you are the project owner, you can merge the PR yourself.


1.4. Setup pre-commit hooks locally 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that ``pre-commit`` is passing, let's setup ``pre-commit`` hooks locally and in GitHub CI that they are automatically run when you push a commit to the remote repository.

#. Type ``git checkout main && git pull upstream main`` to sync with the ``main`` branch.

#. Type ``pre-commit install`` to install the pre-commit hooks locally.

1.5 Setup pre-commit hooks via GitHub CI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, you will setup ``pre-commit CI`` app via GitHub Actions. This CI will run each time a new PR is created.

.. include:: snippets/github-pre-commit-setup.rst

Congratulations if you have successfully passed all the pre-commit hooks! You can now proceed to the next section.

.. _migration-workflow:

2. Migration workflow
---------------------

Here, you will first check the correct folder structure. If the project structure is good, you will create a new project using ``scikit-package``, and then you will migrate existing files from the old project to the new project directory.

.. Attention:: Please read the following carefully before proceeding:

    - Do NOT delete/remove any files before confirming that it is absolutely unnecessary. Create an issue or contact the maintainer.

    - Do NOT delete project-specific content such as project descriptions in README, license information, authors, tutorials, examples.

2.1. Setup correct folder structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Sync with the ``main`` branch by typing ``git checkout main && git pull upstream main``.

#. Before migration, we want to make sure your existing package is structured as a standard recommended Python.

    For a standard package, it should be structured as follows:

    .. code-block::

        my-package/
        ├── src/
        │   ├── my_package/
        │   │   ├── __init__.py
        │   │   ├── file.py
        │   │   ├── ...
        ├── tests/
        │   ├── test_file.py
        │   ├── ...
        ├── ...

    For a namespace package, it should be structured as follows:

    .. code-block::

        diffpy.utils/
        ├── src
        │   ├── diffpy
        │   │   ├── __init__.py
        │   │   └── utils
        │   │       ├── __init__.py
        │   │       ├── file.py
        │   │       ├── ...
        ├── tests/
        │   ├── test_file.py
        │   ├── ...
        ├── ...

#. Is your package structured as above? If yes, skip to the next section in starting a new project with scikit-package :ref:`here<migration-guide-start-new-project>`.

#. Type ``git checkout -b structure`` to create a new branch. In this branch, you will ensure ``src`` and ``tests`` are correctly structured.

#. If your project is structured as ``my-package/my-package/<code>``, run ``git mv <package-name> src``. Your project should now be structured as ``my-package/src/<code>``.

#. Run ``pytest`` locally to ensure the tests are running as expected.

#. Run ``git add src`` and ``git commit -m "skpkg: src to the top level of the package directory"``

#. You can run ``git mv my-package src`` to rename the directory.

#. You will now move ``tests`` to the top level of the package directory ``../my-package/tests/<code>``. If your tests files are located inside ``src``, ensure you use ``git mv src/tests .``.

#. Type ``git add tests`` and ``git commit -m "skpkg: tests to the top level of the package directory"``.

#. Push the changes to a new branch and create a PR to ``package``.

.. _migration-guide-start-new-project:

2.2. Start a new project
^^^^^^^^^^^^^^^^^^^^^^^^

#. Type ``package create public`` and answer the questions provided in :ref:`here<level-5-user-input>`.


2.3. Move ``src``, ``tests``, ``requirements`` to setup GitHub CI in PR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Type ``ls``. Notice there is a new directory named ``<project-name>``. We will call this new directory as the Level 5 directory.

#. Type ``cd <project-name>``. Type ``pwd`` and expect you are inside the directory e.g., ``~/dev/diffpy.pdfmorph/diffpy.pdfmorph``

#. Type ``mv ../.git .`` to move ``.git`` to the re-packaged directory created by ``scikit-package``. Please note that there is a ``.`` in ``mv ../.git .``.

#. Type ``git status`` to see a list of files that have been (1) untracked, (2) deleted, (3) modified.

    - ``untracked`` are new files created by the ``scikit-package``

    - ``deleted`` are files in the original directory but the files that are not in the re-packaged directory. Most of the ``src`` and ``tests`` and doc files will be in this category. We will move them from the original to the re-packaged directory in the next few steps.

    - ``modified`` are files that that exist both in the original and the re-packaged directory, while the scikig-package has made changes to them.

#. Type ``git checkout -b setup-CI`` to create a new branch.

#. Notice there is a ``requirements`` folder containing ``pip.txt``, ``tests.txt``, ``docs.txt``, ``conda.txt``. List dependencies. For ``pip.txt`` and ``conda.txt``, you will most likely have the same dependencies listed. Please check the FAQ section on why we provide both ``pip.txt`` and ``conda.txt`` files :ref:`here<faq-dependency-files>`.

#. Type ``git add requirements && git commit -m "skpkg: create requirements folder"``.

#. Now you will move ``src`` and ``tests`` folders in the following steps.

#. Type ``cp -n -r ../src .`` to copy the source code from the ``main`` to the sk-packaged directory, without overwriting existing files in the destination.

#. Type ``cp -n -r ../tests .``.

#. Run ``git diff`` and the differences

#. Then run ``pytest`` locally to ensure the tests are running as expected.

#. Type ``git add src && git commit -m "skpkg: move src folder"``.

#. Type ``git add tests && git commit -m "skpkg: move tests folder"``.

#. Type ``git add .github && git commit -m "skpkg: move and create github CI and issue templates"``.

    .. Attention::
        If your package does not support Python 3.13, you will need to specify the Python version supported by your package. Follow the instructions here to set the Python version under ``.github/workflows`` :ref:`here <github-actions-python-versions>`


#. Push the changes to the ``CI`` branch by typing ``git push origin CI``.

#. Create a PR from ``CI`` to ``package``. The pull request title can be ``skpkg: move src, tests and setup requirements folder to setup CI``.

#. Notice there is a CI running in the PR. Once the CI is successful, review the PR merge to ``package``.

2.4. Move configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Sync with the ``package`` branch by typing ``git checkout package && git pull upstream package``.

#. Copy all configuration files that are, ``.codecov.yml``, ``.flake8``, ``.isort.cfg``, ``.pre-commit-config.yaml`` files from the main repo to the scikit-package repo.

2.5. Move rest of text files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Files showing as (2) "deleted" upon git status are in the main repo but not in the scikit-package repo. We took care of most of these by moving over the src tree, but let's do the rest now. Go down the list and for <filename> in the ``git status`` "delete" files type ``cp -n ../<filepath>/<filename> ./<target_filepath>``. Do not move files that we do not want. If you are unsure, please confirm with Project Owner.

#. Files that have been (3) modified exist in both places and need to be merged **manually**. Do these one at a time. Differences will show up. Select anything you want to inherit from the file in the main repo. For example, you want to copy useful information such as LICENSE and README files.

.. _scikit-package-workflow-doc:

3. Documentation workflow
--------------------------

3.1. Move documentation files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. We want to copy over everything in the ``doc/<path>/source`` file from the old repo to the ``doc/source`` file in the new repo.

#. If you see this extra ``manual`` directory, run ``cp -n -r ../doc/manual/source/* ./doc/source``.

#. If files are moved to a different path, open the project in PyCharm and do a global search (ctrl + shift + f) for ``../`` or ``..`` and modify all relative path instances.

#. Any files that we moved over from the old place, but put into a new location in the new repo, we need to delete them from git. For example, files that were in ``doc/manual/source/`` in the old repo but are not ``doc/source`` we correct by typing ``git add doc/manual/source``.

3.2. Render API documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: snippets/doc-api-create.rst

3.3. Build documentation locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. include:: snippets/doc-local-build.rst

.. _scikit-package-workflow-cleanup:

4. Clean up
-----------

4.1. Check LICENSE and README
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. For the ``package`` branch, make a ``<branchname>.rst`` file by copying ``TEMPLATE.rst`` in the news folder and under "fixed" put ``Repo structure modified to the new diffpy standard``

#. Check the `README` and make sure that all parts have been filled in and all links resolve correctly.

#. Run through the documentation online and do the same, fix grammar and make sure all links work.

#. Recall in your local, you are currently in the re-packaged directory.

4.2. Clean up the old directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Then rename the old directory to ``mv ../../<package-name> ../../<package-name>-old``. You will have then ``user/dev/<package-name>/<package-name>`` and ``user/dev/<package-name>-old/<package-name>``.

#. Type ``../..`` to go back to the ``dev`` directory.

#. Type ``git clone <https://github.com<org-name>/<project-name>``.

#. Test your package by running ``pytest``.

    .. include:: snippets/pytest-run-local.rst

#. Good to go! Once the test is successful, you can delete the old directory by typing ``rm -rf <package-name>-old``.

Ready for public release?
--------------------------

Congratulations! Your package has been successfully migrated. This has been the most challenging step. Now, let's release your package to PyPI and conda-forge. Please visit the :ref:`Release your package <pypi-release-guide>` page to learn how to release your package!
