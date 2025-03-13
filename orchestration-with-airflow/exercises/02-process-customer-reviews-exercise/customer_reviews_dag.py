from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import os
import csv


@dag(
    "customer_reviews_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="* * * * *",
    catchup=False,
    description="Review average score",
)
def customer_reviews_dag():

    @task
    def extract_reviews():
        pg_hook = PostgresHook(postgres_conn_id="postgres_rental_site")

        context = get_current_context()
        execution_date = context["execution_date"]
        start_of_minute = execution_date.replace(second=0, microsecond=0)
        end_of_minute = start_of_minute + timedelta(hours=1)

        query = f"""
            SELECT review_id, listing_id, review_score, review_comment, review_date
            FROM customer_reviews
            WHERE review_date >= '{start_of_minute.strftime('%Y-%m-%d %H:%M:%S')}'
              AND review_date < '{end_of_minute.strftime('%Y-%m-%d %H:%M:%S')}'
        """

        # TODO: Read data from Postgres, and write the results

    spark_etl = SparkSubmitOperator(
        task_id="spark_etl_reviews",
        application="dags/spark_etl_reviews.py",
        name="guest_reviews_etl",
        application_args=[
            # TODO: Set input and output paths
            "--customer_reviews", "",
            "--output_path", ""
        ],
        conn_id='spark_rental_site',
    )

    extract_task = extract_reviews()
    extract_task >> spark_etl

dag_instance = customer_reviews_dag()