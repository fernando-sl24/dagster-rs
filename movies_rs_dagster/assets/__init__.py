from dagster import load_assets_from_package_module
from . import core
from . import recommender

from dagster_airbyte import build_airbyte_assets
from dagster_dbt import load_assets_from_dbt_project
from dagster import file_relative_path

airbyte_movies_asset = build_airbyte_assets(
    connection_id="44ddfcd7-307d-485a-b9b3-180ba98812dc",
    destination_tables=["movies"],
    asset_key_prefix=["public"],
)

airbyte_scores_asset = build_airbyte_assets(
    connection_id="a55fb929-b2c4-4da2-ade8-cf1645bc45e4",
    destination_tables=["scores"],
    asset_key_prefix=["public"],
)

airbyte_users_asset = build_airbyte_assets(
    connection_id="29ffb500-71ec-4909-bdf9-3018b9671966",
    destination_tables=["users"],
    asset_key_prefix=["public"],
)



DBT_PROJECT_DIR = file_relative_path(__file__, "../../../dbt_project")
DBT_PROFILES_DIR = "/home/fernando/.dbt/"
dbt_assets = load_assets_from_dbt_project(
                    DBT_PROJECT_DIR, 
                    DBT_PROFILES_DIR, 
                    )

core_assets = load_assets_from_package_module(
    package_module=core, group_name='core',
    
)

recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)