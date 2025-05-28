At the moment, the GitHub repository is empty. Let's create a local branch called ``main`` and upload this local branch to the remote GitHub repository.

#. Follow the series of steps to initialite ``Git``, create a new branch called ``main`` in the local repository and push the branch to the remote GitHub repository:

    .. code-block:: bash

        $ git init
        $ git add README.md   # If you are using Level 4
        $ git add README.rst  # If you are using Level 5
        $ git commit -m "docs: add README"
        $ git branch -M main
        $ git remote add origin <your-github-repo-url>
        $ git push -u origin main

    .. note:: What's ``origin``?

        ``origin`` is the default name for the remote repository under your GitHub account. You can think of it as a nickname for the remote repository. You can also use any other name you like, but ``origin`` is the most common convention. For more, please read :ref:`faq-github-terminology`.

    .. note:: What is ``-u`` next to ``git push``?

        The ``-u`` flag tells Git to set the upstream (remote) branch for the local branch. This means that in the future, you can simply use ``git push`` without specifying the remote and branch name, and Git will know where to push your changes.
