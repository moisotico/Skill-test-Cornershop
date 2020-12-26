# Cornershop's Skill Test for Integrations



## About

The following is part of **Cornershop's backend skill integration test**. The requirements can be read at `instructions.md`. The following instructions require [**Python 3** and **pip**](https://www.python.org/downloads/) installed. 



## Downloading 

- Start by downloading this repo:

  ```shell
  $ cd <path_to_save>
  $ git clone https://github.com/moisotico/Skill-test-Cornershop
  ```

  

## Setting your environment

### API Credentials

- Create a file called `credentials.py`:

  ```shell
  $ cd Skill-test-Cornershop/integrations/richart_wholesale_club/
  $ touch credentials.py
  ```

- Write the following in `credentials.py` and save:

  ```python
  GRAND_TYPE = "client_credentials"
  CLIENT_ID = "mRkZGFjM"
  CLIENT_SECRET = "ZGVmMjMz"
  BASE_URL = "https://integration-skill-test-server.herokuapp.com/"
  ```

### Option 1: Setting Anaconda/ Miniconda 

- If you have **Anaconda** or **Miniconda** installed [(you can get it here)](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), try the following steps:

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

### Script

- Run the  file `ingestion.py` :

  ```shell
  $ python3 ./integrations/richart_wholesale_club/ingestion.py
  ```



## Notes



