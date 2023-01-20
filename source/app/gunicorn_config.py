"""Configuration file for Gunicorn server."""

import os

bind = os.getenv("BIND", "0.0.0.0:8000")
workers = int(os.getenv("WORKERS", 1))
root_folder = os.getenv("ROOT_FOLDER", "/path/to/root/folder/")
media = os.getenv("MEDIA", "media")
tiles = os.getenv("TILES", "tiles")
configuration_folder = os.getenv("CONFIGURATION_FOLDER", "/path/to/root/folder/source/app")

db_pdi = os.getenv("DB_PDI", "postgresql://user:password@my.ip:5432/pdi")

db_cd3 = os.getenv("DB_CD3", "postgresql://user:password@my.ip:5432/epok")

api_key = os.getenv("API_KEY", "superapikey123")

raw_env = [
    "ROOT_FOLDER={0}".format(root_folder),
    "MEDIA={0}".format(media),
    "TILES={0}".format(tiles),
    "CONFIGURATION_FOLDER={0}".format(configuration_folder),
    "DB_PDI={0}".format(db_pdi),
    "DB_CD3={0}".format(db_cd3),
    "API_KEY={0}".format(api_key),
]
wsgi_app = os.getenv("WSGI", "app.wsgi")
capture_output = True
