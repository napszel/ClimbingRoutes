#!/bin/bash

set -e

cd backend-scripts
./download_json.sh
python3 update_database.py
python3 generate_index_html.py
python3 generate_beta_index_html.py
./upload_to_atom.sh "$1"
