import os
import sys

import yaml

with open('env_variables.yaml', 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        env = data['env_variables']

        print('Setting env variables...')
        os.environ['POSTGRES_PASSWORD'] = env['POSTGRES_PASSWORD']
        os.environ['POSTGRES_HOST'] = '127.0.0.1'

        print('Running migrations...')
        migrate_command = 'python memorial/manage.py migrate'
        os.system(migrate_command)

        print('Removing env variables...')
        del os.environ['POSTGRES_PASSWORD']
        del os.environ['POSTGRES_HOST']
        sys.exit()

    except yaml.YAMLError as err:
        print(err)
