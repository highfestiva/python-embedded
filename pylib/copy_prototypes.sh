#!/bin/bash

mkdir prototypes
mkdir sitepkgs
mkdir sitepkgs/trabant
rm prototypes/*
rm sitepkgs/trabant/*
cp `ls ~/pd/trabantsim/prototypes/*.py | grep 'prototypes/[a-z]'` prototypes/
cp ~/pd/trabantsim/prototypes/trabant/*.py sitepkgs/trabant/
