from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('example_dag',
         start_date=datetime(2021, 1, 1),
         max_active_runs=3,
         schedule_interval='@daily',  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    start_task = DummyOperator(
        task_id='start_task'
    )

    task_being_checked = BashOperator(
        task_id='task_being_checked',
        bash_command='sleep 30'
    )

    end_task = DummyOperator(
        task_id='end_task'
    )

    start_task >> task_being_checked >> end_task

