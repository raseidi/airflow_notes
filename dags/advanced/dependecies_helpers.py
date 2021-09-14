from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.models.baseoperator import cross_downstream, chain

from datetime import datetime

default_args = {
    'start_date':datetime(2021, 1, 1)
}
with DAG('dependency', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2')
    t3 = DummyOperator(task_id='t3')
    
    t4 = DummyOperator(task_id='t4')
    t5 = DummyOperator(task_id='t5')
    t6 = DummyOperator(task_id='t6')
    
    
    '''
    - big shift operator
    t2.set_upstream(t1) == t2 << t1
    t1.set_downstream(t2) == t1 >> t2

    - cross dependencies
    [t1, t2, t3] >> [t4, t5, t6] # you cant trade dependencies between lists
    [t1, t2, t3] >> t4; [t1, t2, t3] >> t5 # both methods work but it is not suitable
    the correst way is using cross_downstream
    '''
    # cross_downstream([t1, t2, t3], [t4, t5, t6])
    # # another example, now using chain:
    # chain(t1, [t2, t3], [t4, t5], t6) # lists depend of t1

    # another example, now using both methods
    # cross_downstream([t2, t3], [t4, t5])
    # # another example, now using chain:
    # chain(t1, t2, t5, t6) # lists depend of t1

    cross_downstream(from_tasks=[t1, t2, t3], to_tasks=[t4, t5, t6])
