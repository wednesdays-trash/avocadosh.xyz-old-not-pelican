Dont forget to run `generate.py` in a cronjob:) dump the following into `/etc/cron.d/avocadosh`:

``` sh
# /etc/cron.d/avocadosh: re-generate html pages from templates and download last.fm collage
SHELL=/bin/sh
0 * * * * www-data cd /var/www/avocadosh.xyz && /usr/local/bin/poetry run python generate.py
```

A `.env` file needs to be present with the following fields:
- LASTFM_API_KEY
- LASTFM_API_SECRET
- COLLAGE_TTF (full path to a `.ttf` file)
