# Client Server Auth

> `TODO` : introduce docker compose to bind different services together

> `TODO` : introduce nginx / caddy to host ui & backend .

> `TODO`: put `exceptions.py`, `utilities.py` and `commandline.py` in Cookiecutter .


## `INDEX`

| Name | Description |
| ---- | ----------- |
| [Introduction](#introduction) | what is the usefulness and purpose of this project |
| [Launch](#launch) | how to launch application on browser |
| [Redis](#redis) | how redis is setip for this project |
| [Outh App Conf](#oauth-app) | how to configure the Oauth app for google sign-in to work |

## Introduction

> The main requirement for google-Oauth in a client-server architechture is that, the client and the server must be on same domain / host .\
That is why we have used `Flask-ApplicationDispatcher` approach with which we are hosting the client/ui with seperate flask application .

#### How is it different from `Flask-VanillaJS2` implementation

- it uses `credentials.json` file procured from GCP.

> NOTE : retrieve `.env` and `credentials.json` file from google-drive : _Personal Project Secrets_

### Resorces 
<em> what resources did i refer </em>

https://medium.com/@pumudu88/google-oauth2-api-explained-dbb84ff97079
https://www.youtube.com/watch?v=NMnaXz6eMeo&t=1203s

`TODO`: **this below link must be visible as an image**\
[auth web flow](./readme_static_resources/oauth_web_flow.png)

---
<br>

## Launch

---
<br>

## Redis
<em>This section focuses on using redis as a docker image .</em>

Here's how to use the Redis Docker image:

1. Pull the Redis Image:

    Open your terminal or command prompt.
    Use the following command to download the latest Redis image from Docker Hub:

```sh
# Code
docker pull redis:latest
```

    This command retrieves the official Redis image. You can also specify a version tag (e.g., redis:7.0) if you need a specific version.

2. Run a Redis Container: 

    After the image is downloaded, run the following command to start a Redis container:

```sh
# Code
docker run -d --name my-redis -p 6379:6379 redis:latest
```

* -d: Runs the container in detached mode (in the background).\
--name my-redis: Assigns the name "my-redis" to the container. You can choose a different name.\
-p 6379:6379: Maps port 6379 on your host machine to port 6379 in the container. Redis listens on port 6379 by default.
redis:latest: Specifies the Redis image to use.

3. Verify Installation: 
    
    Check if the Redis container is running with the following command:

```sh
# Code
docker ps
```

* You should see the "my-redis" container listed.

4. Connect to Redis
    
    To connect to the redis server, you can use the redis-cli tool.
```sh
# Code
docker exec -it my-redis redis-cli
```

5. Optional Configurations:
    Password: Set a password for your Redis instance using the REDIS_PASSWORD environment variable when running the container:
```sh
# Code
docker run -d --name my-redis -p 6379:6379 -e REDIS_PASSWORD=your_password redis:latest
```

* Custom Configuration: Mount a custom redis.conf file to configure Redis:

```sh
# Code
docker run -d --name my-redis -p 6379:6379 -v /path/to/your/redis.conf:/usr/local/etc/redis/redis.conf redis:latest --requirepass your_password
```

When running the server , you need to set the `HOST` and `PORT` of the REDIS cache .
So when running the redis container on your local machine like above , you need to specify the Env variables in following fashion :
```sh
# .env file
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

---
<br>

## OAuth App
<em>This section focuses on how to configure the Google Oauth App .</em>

set the environment variable values 
```sh
# .env file
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```
we have two environment varibales which are specifically used in this implementation

- GOOGLE_CLIENT_ID : client id of the application that we have created .
- GOOGLE_CLIENT_SECRET : client secret of the application that we have created .

we have alreday created a sample application in Ankit's GCP account :
- Project : _Flask Google Login Test_
- Client Name : _Web Client 2_
    - Type : _Web application_

You can use it's client-id and client-secret values in the env variables.

You may also create a new client of type:web-application , similar to the one stated above, & use it's client-id and client-secret . 

---
<br>

##### Important Notes:
- **Redis Stack** :
    If you want to use Redis with extra features like JSON, search, etc., use the redis/redis-stack-server image instead of redis.
- **Persistence** :
    By default, data stored in the Redis container will be lost when the container is removed. To persist data, use a volume mount to store data on your host machine.
