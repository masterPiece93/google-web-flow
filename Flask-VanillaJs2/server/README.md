Google Auth in Flask Server
===========================
<em>This demonstrates how to implement Google Oauth login in a flask Server application .</em>


## Introduction 

- for poc on google auth
    [READ](https://jaggedarray.hashnode.dev/flask-google-login)
    - this will explain about the implementation
    
## Developer Zone

<details>
<br>
<summary><b>Useful Commands</b></summary>

- using a particular python version

    - command : ```pyenv local <python-version>```

    - example :
        ```sh
        pyenv local 3.10
        ```

- creating virtual environment

    - command : ```pyenv virtualenv <name>```

- activating virtual environment

    - command : ```pyenv activate <name>```

- installing requirements

    - command : ```pip install requirements.py<major>.<minor>._.txt```

    - example :
        ```sh
        pip install requirements.py3.10._.txt
        ```
- cleanup

    - delete virtualenv
        - command : ```pyenv virtualenv-delete <venv-name>```


</details>

### How to run the project

**Prerequisites**

1. Pyenv must be installed on your machine
    - It's recommended to also have `Pyenv-Virtualenv` installed as well to ease out your local development
> [Pyenv Installation Guide](https://docs.google.com/document/d/1Rs-dcS3dNhiaah2xhY7xS8U06I1OvQ6xpt2jWnif6uQ/edit?usp=sharing) 

2. Run Redis in docker container .
```sh
# pull latest redis image
docker pull redis:latest
```
```sh
# run container
docker run -d --name my-redis-cache -p 6379:6379 redis:latest
```

**Commands**

- `Makefile` build tool is used to automate project execution .
- use the following command on accessing `help` on all commands
    ```sh
    # lists down help on all available commands
    make help
    ```

On the First run , Execute this :
```sh
# this will do everything for you & run the project
make all
```

Then post this ( on successive runs ), you can use following commands 

```sh
# to run the project
make run
```

```sh
# to execute the tests
make test
```

```sh
# to install the requirements
make install
```

> NOTE : please load the ui on this root url ( for dev env ) : `http/localhost:5000/`

For executing the `client` application as well , we have to run the following command :
```sh
# to run the `client` application along with the server .
make run-combined
```

* since , we aren't using reverse proxy ( Nginx / Caddy ) , we wre using `Application Dispatcher` approach in Flask to serve to seperate applications on same domain .

### Project Structure

```
.
├── app.py
├── Makefile
├── README.md
├── requirements.py3.10._.txt
├── setup
│   ├── config.py
│
└── src
    ├── v1
    ├── v2
    ├── generic_routes.py
```

- `app.py` contains the flask application creation & setup .
    - major highlights of this file :
        1. loading the config ( which is directly linked to .env file via config.py file )
        2. registering the routes .

> NOTE : routes & api's are managed through a feature of flask , called - `Blueprints`

- `Makefile` contains project setup & building commands .

- `README` contains project documentation & guide

- `requirements.py3.10._.txt` contains python dependencies 
    - major highlights of this file :
        1. notice the name , it signifies the version of python , this indicates that this file will contain project dependencies with their verisons specified accordingly in tandom with the signified python version on the filename
        2. 

- `config.py` conatins the config variables in exact tandom with the .env file .
    - the `.env` file might have extra variables listed , but for the application to recognize a variable , it must be listed in the `config.py` file as well .
        - we might have some variables , like `TEMP`, `SHELL`, `PWD`, `LANG` , `USER` etc... , which are Operating system specific & you don't need them in application , hence you won't list them in `config.py` file , but DevOps team might maintain them in `.env` file

- `generic_routes.py`contains the api code & url .
    - it conains generic api's like `health` & `api-index`

- `/src` folder is everything about your core api logic and managemnet . you can organise it in any way you like .

- `/setup` folder will contain everything related to project wide configuration and setup
    - you can keep `seed_data` related files
    - you can keep some `scripts` that needed pre-/post- or during project execution

### How to do development

`TODO: PENDING`

### Container Setup

`TODO: PENDING`

## Issues Faced

> 1. google.auth.exceptions.InvalidValue: Token used too early, Check that your computer's clock is set correctly.

- https://github.com/googleapis/google-api-python-client/issues/1648
- https://github.com/googleapis/google-auth-library-python/issues/889

> 2. not able to include `client` application , for the purpose of adding it to application dispatcher

- added the outside folder to the PYTHONPATH
    ```python
    # app.py

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    from client.app import create_app
    ```

