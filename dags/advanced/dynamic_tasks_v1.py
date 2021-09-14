from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator

from groups.process_tasks import process_tasks
from datetime import datetime, timedelta

partners = {
    'partner_snowflake': {
        'name': 'snowflake',
        'path': '/partners/snowflake'
    },
    
    'partner_netflix': {
        'name': 'netflix',
        'path': '/partners/netflix'
    },
    
    'partner_astronomer': {
        'name': 'astronomer',
        'path': '/partners/astronomer'
    },
    
}

default_args = {
    'start_date':datetime(2021, 1, 1)
}
@dag(
    description='DAG in charge of processing customer data',
    # start_date=datetime(2021, 1, 1), 
    default_args=default_args,
    schedule_interval='@daily', 
    dagrun_timeout=timedelta(minutes=10), 
    tags=['data_science', 'customers'], 
    catchup=False,  max_active_runs=1,
)
def dynamic_tasks():
    start = DummyOperator(task_id='start')
    for partner, details in partners.items():
        @task.python(task_id=f'extract_{partner}', do_xcom_push=False, multiple_outputs=True)
        def extract(partner_name, partner_path):
            return {'partner_name': partner_name, 'partner_path': partner_path}

        extracted_values = extract(details['name'], details['path']) # this returns an xcom
        start >> extracted_values # ToDo: see when we can establish this kind of dependecy
        process_tasks(extracted_values) # here we get an error since we cant have multiple tasks groups with same id
        # add add_suffix_on_collision on process_tasks to solve this problem

dag = dynamic_tasks()