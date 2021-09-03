from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.subdag import SubDagOperator

from subdag.subdag_factory import subdag_factory
from datetime import datetime, timedelta

@task.python(task_id='extract_partners', do_xcom_push=False, multiple_outputs=True)
def extract():
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    return {'partner_name': partner_name, 'partner_path': partner_path}

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
def sub_dags():
    # partner_settings = extract()
    process_tasks = SubDagOperator(
        task_id='process_tasks',
        subdag=subdag_factory('sub_dags', 'process_tasks', default_args), # this argument expects a dag
        mode='reschedule',
    )
    extract() >> process_tasks

dag = sub_dags()