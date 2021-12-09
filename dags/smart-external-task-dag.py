from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from plugins.smart_external_task_sensor import SmartExternalTaskSensor

with DAG('smart_external_task_dag',
         start_date=datetime(2021, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    start_task = DummyOperator(
        task_id='start_task'
    )

    external_task_check = SmartExternalTaskSensor(
        task_id='external_task_check',
        external_dag_id='example_dag',
        external_task_id='task_being_checked',
        execution_date='{{ ds }}',
        execution_date_fn=True,
        failed_states=['skipped', 'failed'],
        check_existence=True
    )

    end_task = DummyOperator(
        task_id='end_task'
    )

    start_task >> external_task_check >> end_task


