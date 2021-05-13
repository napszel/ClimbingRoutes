#!/bin/bash

set -e

date=$(date +%Y%m%d)

curl -f -g -s 'https://gyms.vertical-life.info/en/gaswerk-schlieren/iframe' >../daily-saves/$date-gas-routes.html || echo Downloading the Gaswerk Routes html failed

curl -f -g -s 'https://gyms.vertical-life.info/en/gaswerk-greifensee/iframe' >../daily-saves/$date-mil-routes.html || echo Downloading the Milandia Routes html failed

curl -f -g -s 'https://gyms.vertical-life.info/en/kletterzentrum-gaswerk-wadenswil/iframe' >../daily-saves/$date-wad-routes.html || echo Downloading the Waedenswil Routes html failed
