#!/usr/bin/env bash

appcfg.py download_app --help;

# appcfg.py --noisy --no_cookies -A souterrain-prod -V v1-0-1 download_app .download/souterrain-prod-v1-0-1;
appcfg.py --noisy --no_cookies -A souterrain-prod -V v-1-0-0 download_app .download/souterrain-prod-v-1-0-0;
appcfg.py --noisy --no_cookies -A souterrain-prod -V v-1-0-1 download_app .download/souterrain-prod-v-1-0-1;
appcfg.py --noisy --no_cookies -A souterrain-prod -V v-1-0-2 download_app .download/souterrain-prod-v-1-0-2;
