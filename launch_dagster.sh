#!/bin/bash

conda activate dagster-mlops-rs

set -o allexport && source environments/local && set +o allexport

dagster dev
