#!/bin/bash

set -e

date=$(date +%Y%m%d)

curl -f -g -s "http://www.kletterzentrum.com/routenfinder/finder/Route/?tx_kletroute_kletroutefilter%5Baction%5D=doFilter&tx_kletroute_kletroutefilter%5Bfilter%5D%5Bcategory%5D%5B65%5D=0&type=1390811741&tx_kletroute_kletroutefilter[offset]=0&tx_kletroute_kletroutefilter[limit]=1500" >../generated/daily-saves/routes-$date.json || echo Downloading the json failed

