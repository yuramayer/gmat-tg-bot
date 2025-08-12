"""Loading the environment keys for the project"""

import os
from dotenv import load_dotenv


load_dotenv()


def get_checked_env(env_name: str):
    """Environment checker"""
    env = os.getenv(env_name)
    if not env:
        raise RuntimeError(f"The required variable isn't defined: {env_name}")
    return str(env)


TEST_BOT_TOKEN = get_checked_env('TEST_BOT_TOKEN')
PROD_BOT_TOKEN = get_checked_env('PROD_BOT_TOKEN')
CLOUD_S3_ID_KEY = get_checked_env('CLOUD_S3_ID_KEY')
CLOUD_S3_SECRET_KEY = get_checked_env('CLOUD_S3_SECRET_KEY')
BUCKET_NAME = get_checked_env('BUCKET_NAME')
ADMINS = get_checked_env('ADMINS')
STAND = str(os.getenv('STAND'))

if STAND == 'LOCAL':
    BOT_TOKEN = TEST_BOT_TOKEN
elif STAND == 'PROD':
    BOT_TOKEN = PROD_BOT_TOKEN

admins_ids = [int(admin_id) for admin_id in ADMINS.split(',')]
