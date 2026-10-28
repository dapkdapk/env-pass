#!/bin/bash

VERSION="v`poetry version -s`"
git tag $VERSION
git push origin --tags