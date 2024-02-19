OctoDB for Python3
==================

This is a wrapper library to use [OctoDB](http://octodb.io) on Python 3

It is based on [pysqlite3](https://github.com/coleifer/pysqlite3)


### Additional features:  (compared to Python's sqlite3 module)

* User-defined window functions (requires SQLite >= 3.25)
* Flags and VFS an be specified when opening connection
* Incremental BLOB I/O, [bpo-24905](https://github.com/python/cpython/pull/271)
* Improved error messages, [bpo-16379](https://github.com/python/cpython/pull/1108)
* Simplified detection of DML statements via `sqlite3_stmt_readonly`.
* Sqlite native backup API (also present in standard library 3.7 and newer).


Installation
------------

You must install some OctoDB library for this one to work. It can be either
pre-compiled binaries or you can compile it by yourself. You can start with
the [free version](http://octodb.io/en/download.html).


### Installing with pip

```
pip install octodb
```


### Cloning and Building

Optionally you can clone the repo and build it:

```
git clone --depth=1 https://gitlab.com/octodb/octodb-python3
cd octodb-python3
python3 setup.py build install
```


Usage
-----

```python
import octodb
import json
import time

conn = octodb.connect('file:app.db?node=secondary&connect=tcp://server:port')

# check if the db is ready
while True:
    result = conn.cursor().execute("PRAGMA sync_status").fetchone()
    status = json.loads(result[0])
    if status["db_is_ready"]: break
    time.sleep(0.250)

# now we can use the db connection
...
```
