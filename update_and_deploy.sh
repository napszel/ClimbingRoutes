#!/bin/bash

set -e

cd backend-scripts
./download_json.sh
python3 update_database.py
./update_postcounts.py
python3 generate_index_html.py
python3 generate_beta_index_html.py
python3 generate_routesarray_json.py
./upload_to_atom.sh "$1"
