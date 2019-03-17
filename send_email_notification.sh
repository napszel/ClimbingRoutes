#!/bin/bash

set -e

# This script assumes PWD is git root
# First parameter: email password
# Rest of the any number of parameters: where to send the emails

URL="http://napszel.com/climbingroutes"
OLD_FILE=./tmp/old-routes.json
NEW_FILE=./tmp/new-routes.json
DIFF=/tmp/diff_output

mv $NEW_FILE $OLD_FILE
cp ./generated/routes.json $NEW_FILE
diff $NEW_FILE $OLD_FILE > $DIFF || true
if [ -s $DIFF ]; then
    #MILANDIA is "" if Greifensee is not found in diff or "Milandia" otherwise
    MILANDIA="" && [[ `cat $DIFF | grep 'OrtBez.*Greifensee'` ]]  && MILANDIA="Milandia"
    GASWERK="" && [[ `cat $DIFF | grep 'OrtBez.*Schlieren'` ]] && GASWERK="Gaswerk"
    PLACE="$GASWERK $MILANDIA"
    #Save first parameter
    pw=$1
    #Remove first parameter
    shift
    #Send email to the rest of the parameters
    sendemail -q -f climbingroutes@napszel.com -xu printer@risko.hu -xp $pw -t "$@" -u "New routes at $PLACE" -m "Check it out at $URL" -s mail.atom.hu:587
fi
