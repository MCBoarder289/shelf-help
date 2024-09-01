#!/usr/bin/env bash
mkdir -p lambda_package

cp lambda_function.py lambda_package/
cp -r  ./db lambda_package/

pip install --target=lambda_package orjson==3.10.3 sqlalchemy==2.0.32 psycopg2==2.9.9

cd lambda_package

zip -r ../shelf_help_analytics_lambda.zip ./*
