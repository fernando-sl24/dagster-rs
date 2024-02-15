from dagster import Definitions, define_asset_job, AssetSelection, ScheduleDefinition, FilesystemIOManager

from .assets import (
    dbt_assets,
    airbyte_movies_asset,
    airbyte_scores_asset,
    airbyte_users_asset,
    core_assets, recommender_assets
)

from .resources import dbt_local_resource, airbyte_instance

all_assets = [*airbyte_movies_asset,*airbyte_scores_asset,*airbyte_users_asset,*dbt_assets,*core_assets, *recommender_assets] # Usar con build_airbyte_assets


mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'Trabajo FInal - Recommender System - Experimento',
        }            
    },
}
#data_ops_config = {
#    'movies_table': {
#        'config': {
#            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
#            }
#    }
#}

training_config = {
    'keras_dot_product_model': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_data_config = {
    'resources': {
        **mlflow_resources
    },
    #'ops': {
    #    **data_ops_config,
    #}
}

job_training_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}

job_all_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        #**data_ops_config,
        **training_config
    }
}

get_data_job = define_asset_job(
    name='get_data',
    selection=['training_data'],
    config=job_data_config
)

get_data_schedule = ScheduleDefinition(
    job=get_data_job,
    cron_schedule="0 * * * *",  # every hour
)

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)



defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        define_asset_job("full_process", config=job_all_config),
        define_asset_job(
            "only_training",
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ],
    resources={
        "io_manager": io_manager,
        "dbt": dbt_local_resource,
        "airbyte": airbyte_instance           # Usar con build_airbyte_assets
    },
    schedules=[get_data_schedule],
    # sensors=all_sensors,
)

