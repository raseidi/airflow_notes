from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

def _extract(ti): # ti: task instance
    partner_name = 'netflix' # i wanna share this data with _process
    # ti.xcom_push(key='partner_name', value=partner_name) # json serialized by default
    partner_path = '/partners/netflix'
    # return partner_name # it's the same than pushing with xcom
    return {'partner_name': partner_name, 'partner_path': partner_path} # returning multiple values; dont create one xcom connection of each variable, it is not suitable

def _process(ti):
    # partner_name = ti.xcom_pull(key='partner_name', task_ids='extract')
    # partner_name = ti.xcom_pull(key='return_value', task_ids='extract') # you calso ommit the key param, letting only task_ids will work
    partner_settings = ti.xcom_pull(task_ids='extract') # getting multiple values
    print(partner_settings['partner_name'], partner_settings['partner_path'])


with DAG(
    dag_id='xcom',
    description='DAG in charge of processing customer data with XCOM',
    start_date=datetime(2021, 1, 1),
    schedule_interval='@daily',
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'],
    catchup=False, 
    max_active_runs=1,
    ) as dag: 
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract,
        # op_args=['{{ var.json.my_dag_partner.name }}']
    )
    
    process = PythonOperator(
        task_id='process',
        python_callable=_process,
    )

    extract >> process # establishing dependencies; execute extract before process