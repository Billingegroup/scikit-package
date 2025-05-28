.. _codecov-token-setup:

We also want to ensure we report that tests are written for the incoming code and report in the incoming PR as shown below:

.. image:: ../img/codecov-pr.png
   :alt: codecov-in-pr-comment

#. Ensure your GitHub repository is public.

#. Visit https://app.codecov.io/

#. Click :guilabel:`Configure Codecov's GitHub app`.

#. Scroll down, find the repository, and click :guilabel:`Configure`.

#. Scroll down again, copy ``CODECOV_TOKEN``, shown below:

    .. image:: ../img/codecov-token.png
        :alt: codecov-list-github-projects

#. In your GitHub repository, visit :menuselection:`Settings -> Actions -> Secrets and Variables`.

#. Click :guilabel:`New repository secret`.

#. Paste the token value in the previous step and name it as ``CODECOV_TOKEN`` as shown below:

    .. image:: ../img/codecov-github.png
        :alt: codecov-list-github-projects

#. Done. From now on, a new comment will be generated on each PR.
