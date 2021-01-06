import os
import subprocess
import sys
import time

import yaml

with open('backend/env_variables.yaml', 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        env = data['env_variables']

        print('DB Name: {}'.format(env['POSTGRES_CONNECTION_NAME']))
        print('Starting Cloud SQL Proxy...')
        try:
            proxy = subprocess.Popen([
                '/tmp/cloud_sql_proxy -instances={}=tcp:5432'.format(
                    env['POSTGRES_CONNECTION_NAME'],
                ),
            ], shell=True)

            print('Waiting 5 seconds for proxy...')
            time.sleep(5)

            print('Setting env variables...')
            os.environ['POSTGRES_PASSWORD'] = env['POSTGRES_PASSWORD']
            os.environ['POSTGRES_HOST'] = '127.0.0.1'

            print('Running migrations...')
            migrate_command = 'python backend/memorial/manage.py migrate'
            os.system(migrate_command)
        finally:
            print('Killing Cloud SQL Proxy...')
            proxy.terminate()

            print('Removing env variables...')
            del os.environ['POSTGRES_PASSWORD']
            del os.environ['POSTGRES_HOST']
            sys.exit()

    except yaml.YAMLError as err:
        print(err)
