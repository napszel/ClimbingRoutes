#!/bin/bash

set -e

cd backend-scripts
./download_jsons_and_generate_one_new.sh
python3 update_database.py
./update_postcounts.py
python3 generate_index_html.py
python3 generate_beta_index_html.py
python3 generate_routesarray_json.py
python3 generate_beta_routesarray_json.py
./upload_to_atom.sh "$1"
