# Cornershop's Skill Test for Integrations



## About

The following is part of **Cornershop's backend skill integration test**. The requirements can be read at `instructions.md`. The following instructions require [**Python 3** and **pip**](https://www.python.org/downloads/) installed. 



## Downloading 

- Start by downloading this repo:

  ```shell
  $ cd <path_to_save>
  $ git clone https://github.com/moisotico/Skill-test-Cornershop
  ```

  test_data_ingestion

## Setting your environment

### API Credentials

- Create a file called `credentials.py` with the following data:

  ```shell
  $ cd Skill-test-Cornershop/src/richart_wholesale_club/
  $ echo' GRAND_TYPE = "client_credentials"
  CLIENT_ID = "mRkZGFjM"
  CLIENT_SECRET = "ZGVmMjMz"
  BASE_URL = "https://integration-skill-test-server.herokuapp.com/"' > credentials.py
  ```

- Write the following in `credentials.py` and save:

  ```python
  GRAND_TYPE = "client_credentials"
  CLIENT_ID = "mRkZGFjM"
  CLIENT_SECRET = "ZGVmMjMz"
  BASE_URL = "https://integration-skill-test-server.herokuapp.com/"
  ```

### Option 1: Setting Miniconda / Anaconda 

- If you have **Miniconda/Anaconda** installed [(you can get it here)](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), try the following steps:

  ```shell
  $ conda activate cornershop-test
  $ pip install -r requirments.txt
  ```

### Option 2: Setting Virtualenv

- If you prefer **Virtualenv**, try the following steps:

  ```shell
  $ pip install virtualenv
  $ virtualenv cornershop-test
  $ pip install -r requirments.txt
  ```

  

## Running

### Server

- Please follow the instructions at `integration-skill-test-server-master/README.md` to run the Heroku app and API. **Once done, you can run the script**.

### Note: Working with Linux

If working with Linux  some commands might change when running the Heroku app:

- Install *Heroku* and [Log In / Sign up](https://id.heroku.com/login):

  ```shell
  $ curl https://cli-assets.heroku.com/install.sh | sh
  ```

-  We need to install *docker-compose*:

  ```shell
  $ sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  $ sudo chmod +x /usr/local/bin/docker-compose
  ```

- And run it:

  ```shell
  $ cd integration-skill-test-server-master/
  $ docker-compose -f docker-compose.yml build
  $ docker-compose -f docker-compose.yml up web
  ```

### Script

- Run the  file `ingestion.py` :

  ```shell
  $ python3 ./src/richart_wholesale_club/ingestion.py
  ```



## Test

- To test, first we must install **pytest**:

  ```shell
  $ pip install pytest
  ```

- To run the tests:

  ```shell
  $ pytest-3
  ```

- We can also run the test like this: 

  ``` sh
  $ pytest-3 ./src/richart_wholesale_club/test_data_ingestion.py
  ```

