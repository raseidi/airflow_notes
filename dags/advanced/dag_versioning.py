import time
from airflow import DAG
from airflow.decorators import task, dag
# from airflow.operators.python import PythonOperator, BranchPythonOperator
# from airflow.operators.dummy import DummyOperator
# from airflow.sensors.date_time import DateTimeSensor
# from airflow.exceptions import AirflowSensorTimeout, AirflowTaskTimeout
from groups.process_tasks import process_tasks
from datetime import datetime, timedelta

default_args = {
    'start_date':datetime(2021, 1, 1),
}
with DAG('process_dag_1_0_2', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    @task.python
    def t1():
        print('t1')

    @task.python
    def t2():
        print('t2')

    @task.python
    def t3():
        print('te')

    t1() >> t2() >> t3()