#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

# cspell:disable-next-line
SRYEARS=SR20*

rm -rf out/

# cspell:disable-next-line
for year in $SRYEARS
do
    echo $year
    mkdir -p out/mjml/$year
    mkdir -p out/html/$year

    for issue in $year/*
    do
        stem=${issue%.md}
        echo "  "$stem
        ./scripts/render-mjml.py $issue > out/mjml/$stem.mjml
        yarn run mjml out/mjml/$stem.mjml -o out/html/$stem.html
    done
done

./scripts/render-indices.py
./scripts/render-feed.py
