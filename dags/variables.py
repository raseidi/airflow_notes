from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

def _extract(partner_name):
    # true as dict, if false it comes as str; this way you avoid useless connections from .get
    # partner_settings = Variable.get('my_dag_partner', deserialize_json=True)
    print(partner_name)

with DAG(
    dag_id='variables',
    description='DAG in charge of processing customer data',
    start_date=datetime(2021, 1, 1), 
    schedule_interval='@daily', 
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'], 
    catchup=False, 
    max_active_runs=1,
    ) as dag: 
    
    # ok but i dont know exactly what variable are for
    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract,
        # the following do the same avoiding multiple connections, but the jinja template is great
        # op_args=[Variable.get('my_dag_partner', deserialize_json=True)['name']]
        op_args=["{{ var.json.my_dag_partner.name }}"] #Variable.get('my_dag_partner', deserialize_json=True)['name']]
    )
    # config file to hide the value in the UI
    # or put _secret in the key name