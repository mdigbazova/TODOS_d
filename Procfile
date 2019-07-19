release: python MeryPortfolio-project//manage.py migrate
web: gunicorn MeryPortfolio-project.MeryPortfolio.wsgi:jobs --preload --workers=1 --log-file - --log-level debug
