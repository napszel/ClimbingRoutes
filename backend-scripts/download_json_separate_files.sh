#!/bin/bash

set -e

date=$(date +%Y%m%d)

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenseilklettern?routentyp=alle&schwierigkeitsgradBis=1030&schwierigkeitsgradVon=10&sicherungsform=alle&standort=schlieren' >../daily-saves/$date-gas-routes.json || echo Downloading the Gaswerk Routes json failed

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenseilklettern?routentyp=alle&schwierigkeitsgradBis=1030&schwierigkeitsgradVon=10&sicherungsform=alle&standort=greifensee' >../daily-saves/$date-mil-routes.json || echo Downloading the Milandia Routes json failed

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenbouldern?routentyp=alle&schwierigkeitsgradBis=1005&schwierigkeitsgradVon=510&standort=schlieren' >../daily-saves/$date-gas-boulds.json || echo Downloading the Gaswerk Boulders json failed

curl -f -g -s 'https://www.kletterzentrum.com/umbraco/api/routen/getroutenbouldern?routentyp=alle&schwierigkeitsgradBis=1005&schwierigkeitsgradVon=510&standort=greifensee' >../daily-saves/$date-mil-boulds.json || echo Downloading the Milandia Boulders json failed


