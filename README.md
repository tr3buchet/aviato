# use with heroku is easiest
## easy button
#[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/tr3buchet/aviato)

## heroku use example
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"dogs"}' https://aviato.herokuapp.com/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"cats"}' https://aviato.herokuapp.com/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs"]}' https://aviato.herokuapp.com/users
curl -s -H "Content-Type: application/json" -X PUT -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs","cats"]}' https://aviato.herokuapp.com/users/jschwing
curl -s -H "Content-Type: application/json" -X PUT -d '{"name":"cats","users":[]}' https://aviato.herokuapp.com/groups/cats
curl -s https://aviato.herokuapp.com/users/jschwing


# deploying manually
## install
clone the git repo

## run tests
`python tests.py`
`flake8 .`

## run the server
```
# set this to your database url
export DATABASE_URL='sqlite:///:memory:'
export PORT='5000'
python app.py
```

## local use examples
```
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"dogs"}' localhost:5000/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"cats"}' localhost:5000/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs"]}' localhost:5000/users
curl -s -H "Content-Type: application/json" -X PUT -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs","cats"]}' localhost:5000/users/jschwing
curl -s -H "Content-Type: application/json" -X PUT -d '{"name":"cats","users":[]}' localhost:5000/groups/cats
curl -s localhost:5000/users/jschwing
```


