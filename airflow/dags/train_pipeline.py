from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Simple Airflow DAG to run the ML training script periodically
default_args = {
    'owner': 'neurospend',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='neurospend_train_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['neurospend'],
) as dag:

    train_task = BashOperator(
        task_id='train_model',
        bash_command='cd /opt/neurospend && python train_model.py',
    )

    train_task
