
# 🚀Data Engineering Project: Automating a Python SQL Script with Apache Airflow

This document summarizes and documents the complete working steps from setting up a Python SQL script to running it via Airflow on an Arch Linux system with `pyenv` and PostgreSQL. It is suitable for beginners and those looking to teach others.

---

## 📦 Project Overview

- **Goal**: Automate the execution of a Python script that runs SQL on a PostgreSQL database using Apache Airflow.
- **Stack**: Python 3.11 (via `pyenv`), PostgreSQL, SQLAlchemy, Apache Airflow, VS Code
- **System**: Linux or WSL2
---

## ✅ Step-by-Step Guide

### 🔧 1. Environment Setup

#### 1.1 Install `pyenv` and `pyenv-virtualenv`

Follow instructions at [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv) and install `pyenv-virtualenv` as well.

#### 1.2 Install Python 3.11.9 via `pyenv` (3.13 cannot run airflow yet)

```bash
pyenv install 3.11.9
pyenv virtualenv 3.11.9 airflow-venv
pyenv activate airflow-venv
```
    after this the virtual environment for airflow is activated, all commands after should be running under this.

#### 1.3 Set Python Interpreter in VS Code

- Press `Ctrl+Shift+P` → "Python: Select Interpreter"
- Pick: `~/.pyenv/versions/airflow-venv/bin/python`
    
    this ensures all required packages are installed in the specific virtual environment that airflow uses
---

### 🗃️ 2. PostgreSQL Setup

#### 2.1 Ensure PostgreSQL is installed and running

Create a database:

```bash
createdb news_db
```

#### 2.2 Verify with DBeaver or `psql`

Use your preferred client to confirm the database exists.

---

### 🐍 3. Create and Test Python SQL Script

    see 3.2, basic script to create (if not exist) table, and insert a row. the sql script is part of the py script that airflow will run.

#### 3.1 Install required libraries

```bash
pip install sqlalchemy psycopg2-binary
```

#### 3.2 Create `run_sql.py`

In your project folder (e.g. `~/news_pipeline`):

```python
from sqlalchemy import create_engine

def run_sql():
    engine = create_engine('postgresql+psycopg2://postgres@localhost/news_db')

    sql_commands = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO test_table (name) VALUES ('Hello Airflow');
    """

    with engine.connect() as conn:
        for cmd in sql_commands.strip().split(';'):
            if cmd.strip():
                conn.execute(cmd)
    print("✅ SQL commands executed successfully.")

if __name__ == '__main__':
    run_sql()
```

#### 3.3 Run the script

```bash
python run_sql.py
```

Verify the data in the database.

---

### 🌬️ 4. Install and Configure Airflow

#### 4.1 Install Airflow (inside `airflow-venv`)

```bash
export AIRFLOW_VERSION=2.9.1
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "$CONSTRAINT_URL"
```

#### 4.2 Set up Airflow folders

```bash
mkdir -p ~/airflow_dev
export AIRFLOW_HOME=~/airflow_dev
```

Optional: add `export AIRFLOW_HOME=~/airflow_dev` to `~/.bashrc`

#### 4.3 Initialize metadata DB

```bash
airflow db init
```
this is to make sure airflow as a software (although it is not) has a db to store its system data.
#### 4.4 Create an admin user

```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

---

### 🚀 5. Run the DAG

#### 5.1 Start scheduler and webserver

**Terminal 1:**

```bash
export AIRFLOW_HOME=~/airflow_dev
airflow scheduler
```

**Terminal 2:**

```bash
export AIRFLOW_HOME=~/airflow_dev
airflow webserver --port 8080
```

Go to [http://localhost:8080](http://localhost:8080) and log in.

#### 5.2 Create a DAG in `~/airflow_dev/dags/sql_script_dag.py`

make sure it is in the dags folder and select the airflow venv

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'sam',
    'start_date': datetime(2025, 7, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='run_sql_script_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    run_script = BashOperator(
        task_id='run_sql_script',
        bash_command='/home/sam/.pyenv/versions/airflow-venv/bin/python /home/sam/news_pipeline/run_sql.py'
    )
```

#### 5.3 Troubleshooting if DAG does not show up

- Restart the webserver: `airflow webserver --port 8080` 
- Ensure `AIRFLOW_HOME` is correctly set (export AIRFLOW_HOME=~/airflow_dev)
- Check DAG file has `.py` extension and valid syntax
- Run: `airflow dags list`

#### 5.4 Trigger the DAG

1. Find `run_sql_script_dag` in the Airflow UI
2. Click **Trigger DAG**
3. Monitor status and logs

You should see the message: `✅ SQL commands executed successfully.`

---

## 🎉 Result

You have:

- Built a reproducible Airflow setup
- Automated a Python SQL job
- Verified everything with Postgres and Airflow logs

This setup is now ready to be expanded with schedules, branching, logging, and more!

---

