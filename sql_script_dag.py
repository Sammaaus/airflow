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
    schedule_interval=None,  # only run manually
    catchup=False,
) as dag:

    run_script = BashOperator(
        task_id='run_sql_script',
        bash_command='/home/sam/.pyenv/versions/airflow-venv/bin/python /home/sam/news_pipeline/run_sql.py'
    )
