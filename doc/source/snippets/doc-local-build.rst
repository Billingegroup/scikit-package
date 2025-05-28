#. Install the requirements for building the documentation.

    .. code-block:: bash

        $ conda install --file requirements/docs.txt

#. Then we will use an external tool called ``sphinx-reload`` to automatically reload the documentation when you make changes to ``.rst`` files.

    .. code-block:: bash

        $ pip install sphinx-reload

    .. note::

        ``sphinx-reload`` is only available via pip install.

#. A HTML will appear automatically in your browser by running the following command:

    .. code-block:: bash

        $ sphinx-reload doc

    .. seealso::

        Did you encounter ``No module named`` error? Please refer to :ref:`faq-doc-error-no-module-name`.
