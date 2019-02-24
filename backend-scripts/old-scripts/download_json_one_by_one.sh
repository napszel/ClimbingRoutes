#!/bin/bash

set -e

echo '[' >../generated/routes.json.tmp
for i in `seq 0 1 1200`
do
    curl -g -s "http://www.kletterzentrum.com/routenfinder/finder/Route/?tx_kletroute_kletroutefilter%5Baction%5D=doFilter&tx_kletroute_kletroutefilter%5Bfilter%5D%5Bcategory%5D%5B65%5D=0&type=1390811741&tx_kletroute_kletroutefilter[offset]=$i&tx_kletroute_kletroutefilter[limit]=25" | jq -r '.items[]' | sed 's/^}$/},/' >>../generated/routes.json.tmp
done

cat ../generated/routes.json.tmp | head -n -1 > ../generated/routes.json
echo '}]' >>../generated/routes.json
