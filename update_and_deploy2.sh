#!/bin/bash

set -e

cd backend-scripts
./download_htmls.sh
python3 convert_html_to_json.py > ../generated/json_from_html_with_full_names.json
python3 update_database_v3.py
#./update_postcounts.py
python3 generate_index_html.py
python3 generate_routesarray_json.py
./upload_to_atom.sh "$1"
