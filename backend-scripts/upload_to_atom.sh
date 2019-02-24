#!/bin/bash

set -e

cd ..
lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/climbingroutes && put index.html && put routesarray.js" </dev/null >/dev/null
lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/betaclimbingroutes && put beta/index.html && put routesarray.js" </dev/null >/dev/null
