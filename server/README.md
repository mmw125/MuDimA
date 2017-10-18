####Install Dependencies
```sh
$ pip install -r server/environments/requirements.txt
```
####Update Database
```sh
$ python server/news_fetcher.py
```
####Start MuDimA server
```sh
$ python server/app.py
```
####Running Tests
```sh
$ pip install -r server/environments/requirements-test.txt
$ py.test --cov=server --cov-report html
```