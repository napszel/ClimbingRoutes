#!/bin/bash

set -e

date=$(date +%Y%m%d)

# Download all 4 jsons to separate files for safe keeping
curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenseilklettern?routentyp=alle&schwierigkeitsgradBis=1030&schwierigkeitsgradVon=10&sicherungsform=alle&standort=schlieren' >../daily-saves/$date-gas-routes.json || echo Downloading the Gaswerk Routes json failed
# Since they don't return route type in the json, we add it
cat ../daily-saves/$date-gas-routes.json  | jq '[.[]] | .[].ClimbingRoutesRouteType = "Vorsteig"' > ../daily-saves/gas-routes-edited.json

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenseilklettern?routentyp=alle&schwierigkeitsgradBis=1030&schwierigkeitsgradVon=10&sicherungsform=alle&standort=greifensee' >../daily-saves/$date-mil-routes.json || echo Downloading the Milandia Routes json failed
cat ../daily-saves/$date-mil-routes.json  | jq '[.[]] | .[].ClimbingRoutesRouteType = "Vorsteig"' > ../daily-saves/mil-routes-edited.json

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenbouldern?routentyp=alle&schwierigkeitsgradBis=1005&schwierigkeitsgradVon=510&standort=schlieren' >../daily-saves/$date-gas-boulds.json || echo Downloading the Gaswerk Boulders json failed
cat ../daily-saves/$date-gas-boulds.json  | jq '[.[]] | .[].ClimbingRoutesRouteType = "Boulder"' > ../daily-saves/gas-boulds-edited.json

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenbouldern?routentyp=alle&schwierigkeitsgradBis=1005&schwierigkeitsgradVon=510&standort=greifensee' >../daily-saves/$date-mil-boulds.json || echo Downloading the Milandia Boulders json failed
cat ../daily-saves/$date-mil-boulds.json  | jq '[.[]] | .[].ClimbingRoutesRouteType = "Boulder"' > ../daily-saves/mil-boulds-edited.json

# Merge all jsons to one file for furher processing
jq -s '[.[]] | flatten' ../daily-saves/{mil,gas}-{boulds,routes}-edited.json >../generated/routes.json


