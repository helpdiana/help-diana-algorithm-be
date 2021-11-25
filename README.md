# help-diana-algorithm-be

## 1. environtment
* FastAPI
* python 3.8.x (tested on 3.8.10)

## 2. install

* Make your virtual envorionment
```bash
$ python -m venv <your-virtual-env-name>
$ source <your-virtual-env-name>/bin/activate
```

* Install modules on your virtual environment
```bash
$ pip install -r requirements.txt
# for tokenizer
$ pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_scibert-0.4.0.tar.gz
```

## 3. Execute

* develop
```
uvicorn main:app --host=0.0.0.0 --port=8000 --reload
```
* production
```
$ gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon

```
## 4. DOCS
1. Execute server(local)
2. Goto http://127.0.0.1/docs
3. swagger
## Reference
* scipacy[https://allenai.github.io/scispacy/]
