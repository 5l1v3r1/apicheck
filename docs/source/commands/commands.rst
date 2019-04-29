
ac-y2j
======

.. _ac_y2j:

This command convert a content from YAML format to JSON with indent option.

Usage examples:

.. code-block:: console

    > ac-y2j petstore-swagger.yaml
    [ ... JSON CONTENT ... ]

.. code-block:: console

    > ac-y2j petstore-swagger.yaml > petstore-swagger.json

.. code-block:: console

    > cat petstore-swagger.json | ac-j2y -P
    [ ... INDENTED JSON CONTENT ... ]


ac-j2y
======

.. _ac_j2y:

This command convert a content from JSON format to YAML.

Usage examples:

.. code-block:: console

    > ac-j2y petstore-swagger.json
    [ ... YAML CONTENT ... ]

.. code-block:: console

    > ac-j2y petstore-swagger.json > petstore-swagger.yaml

.. code-block:: console

    > cat petstore-swagger.json | ac-j2y  > petstore-swagger.yaml
