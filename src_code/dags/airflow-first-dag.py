from airflow import DAG
#from airflow.operators.bash_operator import BashOperator
#from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

start_date = datetime.now().date()

default_args = {
	'owner': 'airflowETL',
	'depends_on_past': False,
	'start_date': str(start_date),
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

dag = DAG('ETL', default_args=default_args, schedule_interval='* */3 * * *', concurrency=1, max_active_runs=1, catchup=False    is_paused_upon_creation=True)


t1 = BashOperator(
	task_id='ETL-pipeline',
	bash_command='python /opt/airflow/scripts/helloairflow.py',
	dag=dag)
