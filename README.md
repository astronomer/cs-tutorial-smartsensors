# Smart Sensors

Showcasing two types of smart sensors: SmartExternalTaskSensor and SmartFileSensor

## Description
The smart sensor is a service (run by a builtin DAG) which greatly reduces Airflow’s infrastructure cost by consolidating multiple instances of small, light-weight Sensors into a single process.
Instead of using one process for each task, the main idea of the smart sensor service is to improve the efficiency of these long running tasks by using centralized processes to execute those tasks in batches.


## Getting Started

### Installing

In order to run these demos on your localhost, be sure to install:

* [Docker](https://www.docker.com/products/docker-desktop)

* [Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/resources/cli-reference)


### Executing demos

Clone this repository, then navigate to the ```cs-tutorial-smartsensors``` directory and start your local Airflow instance:
```
astro dev start
```

In your browser, navigate to ```http://localhost:8080/```

* Username: ```admin```

* Password: ```admin```

### Using the example DAGs
#### 1. Turn on the smart_sensor_group_shard_0 DAG:
The following settings which are contained in the Dockerfile will automatically create a `smart_sensor_group_shard_0` DAG. 
When the smart sensor mode is enabled, a special set of builtin smart sensor DAGs (named `smart_sensor_group_shard_xxx`) is created by the system; These DAGs contain SmartSensorOperator task and manage the smart sensor jobs for the airflow cluster. The SmartSensorOperator task can fetch hundreds of ‘sensing’ instances from sensor_instance table and poke on behalf of them in batches.
```
ENV AIRFLOW__SMART_SENSOR__USE_SMART_SENSOR=True
ENV AIRFLOW__SMART_SENSOR__SHARD_CODE_UPPER_LIMIT=10000
ENV AIRFLOW__SMART_SENSOR__SHARDS=1
ENV AIRFLOW__SMART_SENSOR__SENSORS_ENABLED=SmartFileSensor,SmartExternalTaskSensor
```

#### 2. The smart-file-sensor-dag.py DAG:
To successfully run the `smart-file-sensor-dag` example DAG, create a connection in the airflow UI with the following settings:
- Connection name: `fs_default`
- Connection type: `File(path)`
- In the 'Extra' field, enter: `{"path": "/usr/local/airflow/"}`

Then, turn the DAG on and the SmartFileSensor will check for the file being created by another task in the DAG.

#### 3. The smart-external-task-dag.py and example-dag.py DAGs:
The `smart-external-task-dag` DAG has a task named `external_task_check` which checks the `task_being_checked` task in the `example-dag` DAG. 
Be sure to turn both of these DAGs on, as one DAG is checking against a task in the other DAG, using the SmartExternalTaskSensor operator.



## Additional Resources

* [Apache Airflow - Smart Sensors](https://airflow.apache.org/docs/apache-airflow/stable/concepts/smart-sensors.html)
