from airflow import DAG
from airflow.operators.dummy import DummyOperator
from plugins.smart_file_sensor import SmartFileSensor
from airflow.operators.bash import BashOperator
from datetime import datetime

# For this dag, create a connection in the UI called 'fs_default', File(path) type, and in the 'Extra' field,
# enter: {"path": "/usr/local/airflow/"}

with DAG('smart_file_sensor_dag',
         start_date=datetime(2021, 1, 1),
         schedule_interval='@daily',
         catchup=False
         ) as dag:


    start_task = DummyOperator(
        task_id='start_task'
    )

    # Sleep briefly to allow the file which will be sensed to be created
    sleep_task = BashOperator(
        task_id='sleep_task',
        bash_command='sleep 30'
    )

    # Create a file which the SmartFileSensor tasks will look for before succeeding
    # This file will be created inside of the scheduler container
    create_file = BashOperator(
        task_id='create_file',
        bash_command='touch /usr/local/airflow/file_to_be_sensed.json'
    )

    # Multiple sensors are created here as an example, they are all sensing for the same file
    # being created in the create_file task
    sensors = [
        SmartFileSensor(
            task_id=f'waiting_for_file_{sensor_id}',
            filepath='file_to_be_sensed.json',
            fs_conn_id='fs_default'
        ) for sensor_id in range(1, 4)
    ]

    # Clean up/remove the example file after the sensors succeed
    delete_file = BashOperator(
        task_id='delete_file',
        bash_command='rm /usr/local/airflow/file_to_be_sensed.json'
    )

    end_task = DummyOperator(
        task_id='end_task'
    )

    start_task >> create_file >> end_task
    start_task >> sleep_task >> sensors >> delete_file >> end_task