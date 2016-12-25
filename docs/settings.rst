Settings
========

ROUTING_ENABLED
---------------
.. code-block:: python

    default: True

Will disable the routing if set to False.

ENABLE_PROXY_ROUTING
--------------------
.. code-block:: python

    default: False

Will enable proxy routing if set to True.

.. note::
    read :ref:`caveats<caveats>` before enabling this setting.

ROUTING_CACHE
-------------
.. code-block:: python

    default: False

Will cache the routers and corresponding destinations using `lru_cache` if set to True.
