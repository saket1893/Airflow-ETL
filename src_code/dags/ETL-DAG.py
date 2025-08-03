from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime

# Import functions from your custom scripts (make sure they are in the correct path)
from my_data_pipeline import generate_data, validate_data, load_data

# Define default_args for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 8, 3),  # Adjust the start date as needed
    'catchup': False,
}

# Define the DAG
with DAG(
    'my_data_pipeline',
    default_args=default_args,
    description='Data pipeline to generate, validate, and load data into MySQL',
    schedule_interval=None,  # Set to None or a cron expression if you want it to run periodically
) as dag:

    # Task 1: Generate Data
    t1 = PythonOperator(
        task_id='generate_data',
        python_callable=generate_data,
        op_args=[5],  # Number of records to generate
        provide_context=True,
    )

    # Task 2: Validate Data
    t2 = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        provide_context=True,  # To pass data between tasks
    )

    # Task 3: Load Data to MySQL
    t3 = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_args=[
            'mysql',  # Host: Docker service name
            3306,     # Port
            'airflow',  # Database name
            'airflow',  # User
            'airflowpassword',  # Password
        ],
        provide_context=True,
    )

    # Task 4: Success Task (Optional)
    t4 = PythonOperator(
        task_id='success_task',
        python_callable=lambda: print("Pipeline executed successfully!"),
    )

    # Define task dependencies (T1 > T2 > T3 > T4)
    t1 >> t2 >> t3 >> t4
