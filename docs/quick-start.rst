Quick Start
===========

- installation
- starting dask client/pointing to a dask cluster
- loading the data
- examining the data
    - filters
    - nlp_tools
    - batch_processing
    - classification

Installation
------------

To install murphy on your machine, just install via pip:

```bash
pip install smpa-murphy
```

For more information on installation, check out our :ref:`install guide<installation>`.


Starting up Dask (*optional*)
----------------

Using Dask is optional, and while all of our code is backwards compatible with Pandas, being able to launch your own Dask Cluster or having access to the `Dask Dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>` or `any of it's other use cases <https://stories.dask.org/en/latest/>`

To use Dask, simply import it's Client class and initialize with your configurations

```python
from dask.distributed import Client

client = Client(<your configs here>)
client
```

You can find more information on Dask Client `here <https://distributed.dask.org/en/latest/client.html>`