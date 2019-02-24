#!/bin/bash

set -e

lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/climbingroutes && put ../index.html && put ../javascript.js && put ../style.css && cd generated && put ../generated/routesarray.js" </dev/null >/dev/null
lftp -c "open sftp://napszel:$1@atom.hu && cd public_html/climbingroutes && put ../beta.html && put ../javascript-beta.js && put ../style-beta.css && cd generated && put ../generated/routesarray-beta.js" </dev/null >/dev/null
