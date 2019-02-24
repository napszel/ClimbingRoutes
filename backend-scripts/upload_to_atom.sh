#!/bin/bash

set -e

cd ..
lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/climbingroutes && put generated/index.html && put generated/routesarray.js && put javascript.js && put style.css" </dev/null >/dev/null
lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/climbingroutes && put generated/beta.html && put generated/routesarray-beta.js && put javascript-beta.js && put style-beta.css" </dev/null >/dev/null
