# Flask-Formist

Flask extension for working with WTForms.

It can be used as an alternative for Flask-WTF.

It provides BaseForm for working with CSRF tokens (the Flask app config should have `CSRF_SECRET_KEY` and `CSRF_TIME_LIMIT` keys).

There is also a handle_form function for dealing with forms:
you provide form class, template to be rendered, on_success function to be called when the form is valid, cancel url and object to be edited.


## Installation

```bash
$ pip install Flask-Formist
```

## Usage

First create the `wtf` object:

```python
from flask_formist import Formist
wtf = Formist()
```

Then initialize it using init_app method:

```python
wtf.init_app(app)  # app is your Flask app instance
```


## License

`Flask-Formist` was created by Rafal Padkowski. It is licensed under the terms
of the MIT license.
