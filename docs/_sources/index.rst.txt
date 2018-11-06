Welcome to **Pole Vault**'s documentation
=========================================

The **polevault** python package can be used to encrypt and decrypt entries
in user provided text-based configuration files, containing credentials or
API keys.

For example, if the user has a ``secrets/servers.yml`` file containing:

.. code:: yaml

    server_a:
      address: 192.168.64.1
      username: admin
      password: abc123!

    server_b:
      address: 192.168.64.2
      username: admin
      password: xyz789!

If the user types this command:

.. code-block:: console

    $ polevault encrypt secret secrets/servers.yml
    Encryption key:
    The encryption key is: fp3Hx6zUpFuW8jufDjeneFNWGhGbIkiDFCfXRt0ZS1E

The file will be changed to look something like this:

.. code:: yaml

    server_a:
        encrypted: sAtnD717a2A+nb4326h4+VbkUsGihWzu4DXnp530P008Um/2qNZezfqw+cMCCeMe...

    server_b:
        encrypted: 2nKuLuV/6NwYVne1hZrJF786U8d1hIuCO4ctM7O6vomzjMju/VPssRzMADgPMTJc...

The encryption key that was provided can later be used to decrypt the entries
in the same file, like this:

.. code-block:: console

    $ polevault decrypt secret secrets/servers.yml
    Encryption key: 
    $

After this, the contents of the file will be back the way they were before encrypting.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README
   CHANGELOG
   docsource/api/modules


Indices and Tables:
===================

* :ref:`genindex`
* :ref:`modindex`
