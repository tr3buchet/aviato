[![Build Status](https://travis-ci.org/tr3buchet/aviato.svg?branch=master)](https://travis-ci.org/tr3buchet/aviato)

# use with heroku is easiest
## easy button
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/tr3buchet/aviato)

after the deploy is complete click "view app"

## heroku use example
the name you choose for your app is needed in the urls below. i chose "aviatotest" as you can see.
also I have taken the liberty of leaving aviatotest running so it can be played with
```
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"dogs"}' https://aviatotest.herokuapp.com/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"name":"cats"}' https://aviatotest.herokuapp.com/groups
curl -s -H "Content-Type: application/json" -X POST -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs"]}' https://aviatotest.herokuapp.com/users
curl -s -H "Content-Type: application/json" -X PUT -d '{"first_name":"john","last_name":"schwinghammer","userid":"jschwing","groups":["dogs","cats"]}' https://aviatotest.herokuapp.com/users/jschwing
curl -s -H "Content-Type: application/json" -X PUT -d '{"name":"cats","users":[]}' https://aviatotest.herokuapp.com/groups/cats
curl -s https://aviatotest.herokuapp.com/users/jschwing
```

# deploying manually
## install
`git clone https://github.com/tr3buchet/aviato.git`

## run tests
`python tests.py`
`flake8 .`

## run the server
multiple database types are supported as can be seen in the examples below
```
# set this to your database url
export DATABASE_URL='mysql://user:pass@123.123.123.123:3306'
export DATABASE_URL='postgres://xbcutzpdwbjwxy:tBxOrqyV2v7Ae5Vm6EbcpHFNza@ec2-50-17-253-74.compute-1.amazonaws.com:5432/d92vf2nsn9r8vp'
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


