#!/bin/sh

if [ $# -ne 1 ]; then
    echo "./build.sh version"
    exit 1
fi

rm -rf Envoy-$1.docset
cp -r Envoy.docset-tmpl Envoy-$1.docset
sed -i "" -e "s/VERSION/$1/g" Envoy-$1.docset/Contents/Info.plist
cp -r Documents/$1 Envoy-$1.docset/Contents/Resources/Documents/
./gen.py $1
mv docSet.dsidx Envoy-$1.docset/Contents/Resources/
