while this app is code complete now and easy to run, the data isn't persistent

i will be updating the deploy mechanisms shortly

for now

## install
clone the git repo

## run tests
`python tests.py`

## run the server
`python app.py`

## use examples
```
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"dogs"}' localhost:5000/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"cats"}' localhost:5000/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs"]}' localhost:5000/users
curl -s -H "Content-Type: application/json" -X PUT -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs","cats"]}' localhost:5000/users/jschwing
curl -s -H "Content-Type: application/json" -X PUT -d '{"name":"cats","users":[]}' localhost:5000/groups/cats
curl -s localhost:5000/users/jschwing
```


#[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/tr3buchet/aviato)
