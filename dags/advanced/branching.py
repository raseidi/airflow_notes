import time
from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator

from groups.process_tasks import process_tasks
from datetime import datetime, timedelta

partners = {
    'partner_snowflake': {
        'name': 'snowflake',
        'path': '/partners/snowflake',
        'priority': 2,
        'pool': 'snowflake'
    },
    
    'partner_netflix': {
        'name': 'netflix',
        'path': '/partners/netflix',
        'priority': 3,
        'pool': 'netflix',
    },
    
    'partner_astronomer': {
        'name': 'astronomer',
        'path': '/partners/astronomer',
        'priority': 1,
        'pool': 'astronomer'
    },
    
}

def _choosing_partner_based_on_day(execution_date):
    day = execution_date.day_of_week
    print('DAY!!!')
    print(day)
    if day == 1: # monday
        return 'extract_partner_snowflake'
        
    if day == 3: # wednesday
        return 'extract_partner_netflix'
        
    if day == 5: # friday
        return 'extract_partner_astronomer'

    return 'dummy_stop'
        

default_args = {
    'start_date':datetime(2021, 1, 1),
    'retries': 0
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
def my_dag():
    start = DummyOperator(task_id='start')
    choosing_partner_based_on_day = BranchPythonOperator(
        task_id='choosing_partner_based_on_day',
        python_callable=_choosing_partner_based_on_day,
    )
    stop = DummyOperator(task_id='dummy_stop')
    storing = DummyOperator(task_id='storing', trigger_rule='none_failed_or_skipped')


    choosing_partner_based_on_day >> stop
    for partner, details in partners.items():
        @task.python(task_id=f'extract_{partner}', do_xcom_push=False, multiple_outputs=True)
        def extract(partner_name, partner_path):
            time.sleep(3)
            # raise ValueError('failed')
            return {'partner_name': partner_name, 'partner_path': partner_path}

        extracted_values = extract(details['name'], details['path']) # this returns an xcom
        start >> choosing_partner_based_on_day >> extracted_values

        process_tasks(extracted_values) >> storing # storing will be skipped because multiple parents are skipped

dag = my_dag()