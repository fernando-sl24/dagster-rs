import setuptools
import os

DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.5.7')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.21.7')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.8.0')

setuptools.setup(
    name="movies-rs-dagster",
    packages=setuptools.find_packages(),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        f"dagit=={DAGSTER_VERSION}",
        f"dagster-gcp=={DAGSTER_LIBS_VERSION}",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"dagster-airbyte",
        f"dagster-dbt==0.21.7",
        f"dbt-core<1.7",
        #f"dbt-extractor== 0.5.0",
        f"dbt-postgres<1.7" ,
        #f"dbt-semantic-interfaces==0.4.0",
        f"mlflow=={MLFLOW_VERSION}",
        f"tensorflow",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "jupyter"], "tests": ["mypy", "pylint", "pytest"]},
)


