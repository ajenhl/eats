#!/bin/sh
cd eatsml
ant clean
ant compile
ant dist
cp dist/eatsml.jar ../lookup/lib/
cp dist/eatsml.jar ../oxygen/lib/
cd ../lookup/
ant clean
ant compile
ant dist
cp dist/eatslookup.jar ../oxygen/lib
cd ../oxygen
ant clean
ant compile
ant dist
