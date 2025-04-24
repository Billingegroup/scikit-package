Overview
^^^^^^^^

In this section, you will use ``scikit-package`` to start a new project that is readily installable. This ensures that your code is available across all files on your local computer. Hence, Level 4 is also referred to as ``system``.

By the end of this tutorial, you will also have your package hosted on GitHub, where you will utilize GitHub Actions to run automatic linting and testing for the incoming code in your GitHub repository.

This tutorial should take about 10 to 15 minutes.

Prerequisites
^^^^^^^^^^^^^

For Level 4, we assume you have prior experience in developing scientific code in Python. Additionally, we assume you have hosted at least one project on GitHub. If you are new to GitHub, please refer to the FAQ guide on the GitHub workflow :ref:`here <faq-github-workflow>`.

.. include:: snippets/scikit-installation.rst


Initiate a project with ``scikit-package``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Run the following command to create a new project with ``scikit-package``:

    .. code-block:: bash

        package create system

#. Answer the following questions:

    :project_name: (my-project)

    :github_org: (billingegroup)

    :github_repo_name: (my-project)

    :conda_pypi_package_dist_name: (my-project)

    :package_dir_name: (my_project)

    :project_owner_name: (Simon Billinge)


#. ``cd`` into the project directory created by the ``package create`` command above:

    .. code-block:: bash

        cd <project-name>

#. Done! Let's proceed to the next section to check the folder structure.

Check folder structure
^^^^^^^^^^^^^^^^^^^^^^

#. When you ``cd`` into the new directory, you will see a folder structure as shown below:

    .. code-block:: text

        my-package/
        ├── LICENSE.rst
        ├── README.rst
        ├── environment.yml
        ├── pyproject.toml
        ├── requirements
        │   ├── conda.txt
        │   ├── pip.txt
        │   └── test.txt
        ├── src
        │   └── my_package
        │       ├── __init__.py
        │       └── functions.py
        └── tests
            └── test_functions.py

Install your package locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Build and install the package locally:

    .. code-block:: bash

        pip install -e .

    .. note:: What is the ``-e`` flag?

        ``pip install`` will also install the dependencies listed in ``requirements/pip.txt``. The ``-e`` flag indicates that you want to install the package in "editable" mode, which means that any changes you make to the source code will be reflected immediately without needing to reinstall the package. This is useful for development purposes.

#. Check your package is installed in the conda environment:

    .. code-block:: bash

        pip list

#. Done! Let's now run unit tests with the locally installed package.

Run tests with your locally installed package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Install the testing dependencies for testing.

    .. code-block:: bash

        conda install --file requirements/test.txt

#. Then, run the tests using the following command:

    .. code-block:: bash

        pytest

#. Ensure tests all pass.

#. Notice that in ``tests/test_functions.py``, we are importing the locally installed package.

#. Congratulations! Your package is now available for use in any Python script or Jupyter notebook on your local computer.

#. Done! Let's now learn to automate your code formatting locally.

.. note::

    Why is it required to list dependencies both under ``pip.txt`` and ``conda.txt``? Please refer to the FAQ section :ref:`here<_faq-dependency-management>`.


Automatic code formatting with ``pre-commit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Notice that there is a hidden file called ``.pre-commit-config.yaml`` in the root directory. This file is used to configure pre-commit "hooks". These hooks are checks that can be automatically executed when you commit your code to Git.

.. note::

    If you are not familiar with Git/GitHub, don't worry. Here, we provide step-by-step instructions.

#. Initialize a local Git repository in your project folder:

    .. code-block:: bash

        git init

#. Add your files to the local Git repository:

    .. code-block:: bash

        git add .

#. Format your code by running:

    .. code-block:: bash

        pre-commit run --all-files

#. Ensure that all of the checks pass.

    .. code-block:: text

        black....................................................................Passed
        prettier.................................................................Passed
        docformatter.............................................................Passed

    .. note::

        ``black`` is a tool that automatically formats Python code to conform to the PEP 8 style guide. ``prettier`` is a tool that formats code in various languages, including ``.md``, ``.rst``, and ``.json`` files. ``docformatter`` is a tool that formats docstrings in Python code.


#. Done! You have successfully formatted your code. But, let's also make sure these hooks are triggered automatically when you make a commit.

Trigger pre-commit hooks automatically with Git commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Configure ``pre-commit`` to run each time a new commit is made:

    .. code-block:: bash

        pre-commit install

#. Let's now stage and commit the code:

    .. code-block:: bash

        git add .
        git commit -m "skpkg: start a new project with skpkg system template"

#. Notice that the hooks all pass. You will see the new commit in the git log:

    .. code-block:: bash

        git log

    .. note::

        If one or more of the hooks fail, no commit will be made. But, ``pre-commit`` will automatically lint your code too. If this is the case, simply re-enter the same commit message again.

#. Done. Let's now push your code to GitHub, which is a remote/cloud Git repository.

Create a new project on GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Visit `https://github.com/new <https://github.com/new>`_

#. Choose and enter values for ``Owner`` and ``Repository name``.

#. Choose ``Public`` or ``Private``.

#. Check ``Add a README file``.

#. Set ``None`` under ``Add .gitignore``.

#. Set ``None`` under ``Choose a license``.

#. Click the ``Create repository`` green button to create the repository.

#. Done. Let's push your code from your local Git repository to the remote GitHub repository.

Push your code to GitHub repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Set up the remote GitHub repository. Let's call this repository ``origin``, a common name for the remote repository.

    .. code-block:: bash

        git remote add origin https://github.com/<OWNER>/<project-name>.git

#. Pull the code from the remote ``main`` branch. Recall we had a ``README.md`` file created.

    .. code-block:: bash

        git pull origin main

#. Create a new local branch from the ``main`` branch. Let's call this branch ``skpkg-proj``.

    .. code-block:: bash

        git checkout -b skpkg-proj

    .. note::

        The ``-b`` flag indicates that you want to create a new branch if it does not already exist.


#. Remove the ``README.md`` file. We already have a ``README.rst`` file created with ``scikit-package``.

    .. code-block:: bash

        rm README.md

#. Let's now stage and commit the code.

    .. code-block:: bash

        git add README.md
        git commit -m "chore: remove README.md file pulled from remote main branch"

    .. note::

        You may wonder why we ``git add README.md``. While we removed it from our local computer, we still have to let the local Git repository know manually that it has been removed. Recall that when you run ``git init``, it creates a hidden folder called ``.git`` in your local project directory.

#. Let's now push our code to the new ``skpkg-proj`` local branch and push to the remote ``skpkg-proj`` branch.

    .. code-block:: bash

        git push --set-upstream origin skpkg-proj

#. Visit your remote GitHub repository. You should see the new branch ``skpkg-proj``.

#. Done!

Create a pull request from ``skpkg-proj`` to ``main``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Visit your GitHub repository.

#. Click on the new green button that says ``Compare & pull request``.

#. The PR title can be ``skpkg: start a new project with skpkg system template``.

#. The ``base`` branch should be ``main`` and the ``compare`` branch should be ``skpkg-proj``.

#. Click on the ``Create pull request`` button.

#. Wait for ``Tests on PR`` to run and pass. It runs ``pytest`` on the incoming code in each pull request.

#. While waiting, review the files that are changed. Ensure the only file removed is ``README.md``.

#. Do not merge the PR yet! Let's set up ``pre-commit`` in this GitHub repository as well so that it runs the hooks in each PR.

.. note:: Why do I need to set up ``pre-commit CI``?

    While our code is formatted locally before anything is pushed to the remote repository, it may not be the case for others. Hence, we want to ensure the code is formatted automatically by ``pre-commit`` in each pull request. This is done by setting up ``pre-commit CI`` in the GitHub (remote) repository.


Setup pre-commit CI in GitHub repository for public repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

    ``pre-commit CI`` is FREE for ``public`` repositories. If you are using a private repository, you may skip this section.

.. include:: snippets/github-pre-commit-setup.rst


Merge the pull request
^^^^^^^^^^^^^^^^^^^^^^^

#. Merge the PR.

#. Delete the ``skpkg-proj`` branch after merging.

#. Check that your remote ``main`` branch is updated!

#. Congratulations! You are done with Level 4!


(Optional) How to develop your code moving forward
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assume that you have successfully followed the previous steps. Now, you want to add new code to your GitHub repository. Perhaps you are working with a group of people. Here is a high-level overview with step-by-step instructions on how to do that:

#. Pull the latest code from the remote ``main`` branch:

    .. code-block:: bash

        git checkout main
        git pull origin main

    .. note::

        Recall that we used the name ``origin`` as the nickname for the remote GitHub repository.

#. Ensure that your local ``main`` branch is synced with the remote ``main`` branch by running:

    .. code-block:: bash

        git log

#. Create a new local branch from the ``main`` branch. Let's call this branch ``skpkg-proj``:

    .. code-block:: bash

        git checkout -b <branch-name>

#. Modify any file that you want. Then, stage and commit the changes:

    .. code-block:: bash

        git add <file-modified-added-deleted>
        git commit -m "feat: <your commit message>"

#. Push your code from ``<branch-name>`` to the remote ``<branch-name>`` branch:

    .. code-block:: bash

        git push --set-upstream origin <branch-name>

#. Visit your GitHub repository.

#. Create a PR from ``<branch-name>`` to ``main``.

#. Wait for the ``Tests on PR`` and ``pre-commit`` checks to pass.

#. Merge the PR, delete the branch.

#. Repeat the steps in this section.

#. Done!


What's next?
^^^^^^^^^^^^

.. note::

    Make sure you check out the best practices and Billinge group's guidelines for communications and examples in the FAQ section :ref:`here<frequently-asked-questions>`.


Once you are ready to release your package to the wider world, let's proceed to :ref:`Level 5<start-new-project-package-full>` where you will learn to release your package to PyPI and conda-forge so that your package can be installed by anyone in the world.
