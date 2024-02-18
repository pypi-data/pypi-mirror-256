# Setup the development env unix
```sh
virtualenv venv
. ./venv/bin/activate
```

# Setup the development env win10
```sh
python -m venv venv
. .\venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install pytest
pip install python-dotenv
pip install robotframework-sapguilibrary
copy .\.env.template .\sap_nota_pedido\.env
```

# Publish
python -m venv venv

Test
Unix
rm -rf dist build hnt_sap_nota_pedido_library.egg-info
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
