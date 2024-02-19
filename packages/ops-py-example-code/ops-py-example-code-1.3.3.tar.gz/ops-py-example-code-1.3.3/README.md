# example-code

This repository and code are intended to function as a guide on how Python code in **ops-py-*** repositories should be written, documented and distributed.   

The code in the ops-py-* repositories must be written as Open Source. It will be distributed to https://pypi.org/user/Equinor as PIP packages and made available to the public.  

The file structure in the repo should follow the following standard:   
```
src/
├─ requirements.txt
├─ simple_service/
│  ├─ __init__.py
│  ├─ simple_service.py
README.md
LICENSE
```

### How the code should be written and documented
The code should include comments and proper documentation. **Use Docstrings**   
Please refer to the documentation in [simple_service.py](src%2Fsimple_service%2Fsimple_service.py)
and to [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code)

To write proper and understandable code, for you and for others to read, please also refer to [How to Write Beautiful Python Code With PEP 8](https://realpython.com/python-pep8/)

### How to build and distribute the code
Please refer to the following [documentation](https://github.com/equinor/ops-py/blob/main/docs/python_contribute.md)
