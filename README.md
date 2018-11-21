# discovery01

```
Setup Virtual Environment
```
pip install pipenv (https://realpython.com/pipenv-guide/)
sporn new environemnt 
set python3 export PATH=/usr/local/lib/python3.6/libexec/bin:$PATH
1. setup Pipfile
2. `pipenv install`
3. `pipenv shell`


```
running app
```
$ export FLASK_APP=app.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/

``` 
Structure (:why)
```
* "home page": read blogs
* "Contact us": feedback loop for reads
* "Admin portal": for the administrator to write to the world
* * "login page" 
* * "write blogs" 
* * "page to view stats" 
* "Blog template": page for each blog

```
Potential Idea's for frontend
```
1. Comment area ("blog template")
2. Ribbon over blogs to control sorting / filtering ("home page")
3. Search page


```
DATABASE updates
```
1. create the migration script and confirm using the following for generation
`python manage.py db migrate -m "20181121_v1_change"`
2. Confirming the migration script in `/migrations/versions/...py` kick it off
`python manage.py db upgrade`







