![](https://raw.githubusercontent.com/CheeseCake87/Quart-Imp/master/_assets/quart-Imp-Small.png)

# Quart-Imp

[![PyPI version](https://img.shields.io/pypi/v/quart-imp)](https://pypi.org/project/quart-imp/)
[![License](https://img.shields.io/badge/license-LGPL_v2-red.svg)](https://raw.githubusercontent.com/CheeseCake87/quart-imp/master/LICENSE)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

`pip install quart-imp`

## What is Quart-Imp?

Quart-Imp's main purpose is to help simplify the importing of blueprints, resources, and models.
It has a few extra features built in to help with securing pages and password authentication.

## Note

**Quart-Flask-Patch is required to use Quart-Imp.**

## Generate a Quart app

```bash
quart-imp init
```

## Example

```text
project/
└── app/
    ├── blueprints/
    │   └── www/...
    ├── extensions/
    │   └── __init__.py
    ├── resources/
    │   ├── static/...
    │   ├── templates/...
    │   └── routes.py
    └── __init__.py
```

`# app/extensions/__init__.py`

```python
import quart_flask_patch
from flask_sqlalchemy import SQLAlchemy

from quart_imp import Imp

_ = quart_flask_patch

imp = Imp()
db = SQLAlchemy()
```

`# app/__init__.py`

```python
from quart import Quart

from app.extensions import imp, db


def create_app():
    app = Quart(__name__, static_url_path="/")

    imp.init_app(app)
    imp.import_app_resources(
        files_to_import=["*"],
        folders_to_import=["*"]
    )
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    @app.before_serving
    async def create_tables():
        db.create_all()

    return app
```
