from datetime import datetime
from dags.advanced.dynamic_dags import generate_dag

partners = {
    'snowflake': {
        'schedule': '@daily',
        'path': '/data/snowflake'
    },
    'netflix': {
        'schedule': '@weekly',
        'path': '/data/netflix'
    }, 
}

for partner, details in partners.items():
    dag_id = f'dynamid_dag_{partner}'
    print(dag_id)
    default_args = {
        'start_date': datetime(2021, 1, 1)
    }
    globals()[dag_id] = generate_dag(dag_id, details['schedule'], details, default_args)