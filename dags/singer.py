from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import os

# Name dag_id the filename so changes down the line won't cause confusion
dag_id = os.path.basename(__file__).replace('.py','')
# Location of our singer config files and bash script
script_path = '~/airflow-on-singer/scripts/'
# Output for target-csv extractions
tmp_path = '/tmp/klaviyo_output'
# Location of shell script to install tap-klaviyo, target-csv, and target-postgres in its own virtualenv. Create temp folders to store data.
create_venv_command = f'{script_path}create_venv.sh '

# Pipeline
default_args = {
    'owner': 'fran',
    'depends_on_past': False,
    'start_date': datetime(2020,12,16),
    'email': ['fran@francescao.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id=dag_id,
    default_args=default_args,
    dagrun_timeout=timedelta(minutes=30),
    schedule_interval='@daily'
) as dag:

    # Create virtual environments and temp folder
    create_venv = BashOperator(
        task_id = 'create_venv',
        bash_command = create_venv_command
    )

    # Push klaviyo data to CSV
    klaviyo_load_csv = BashOperator(
        task_id = 'klaviyo_load_csv',
        bash_command = f'~/.virtualenv/tap-klaviyo/bin/tap-klaviyo --config {script_path}/tap-klaviyo/config.json --state {script_path}/tap-klaviyo/state.json --catalog {script_path}/tap-klaviyo/catalog.json | ~/.virtualenv/target-csv/bin/target-csv --config {script_path}/target-csv/config.json'
    )

    # Push klaviyo data to Postgres
    klaviyo_load_postgres = BashOperator(
        task_id = 'klaviyo_load_postgres',
        bash_command = f'~/.virtualenv/tap-klaviyo/bin/tap-klaviyo --config {script_path}/tap-klaviyo/config.json --state {script_path}/tap-klaviyo/state.json --catalog {script_path}/tap-klaviyo/catalog.json | ~/.virtualenv/target-postgres/bin/target-postgres --config {script_path}/target-postgres/config.json'
    )

    # Dummy task to mark completion
    all_done = DummyOperator(
        task_id = 'all_done'
    )

    create_venv >> [klaviyo_load_csv,klaviyo_load_postgres] >> all_done