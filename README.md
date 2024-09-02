## NeuesVomTage News Aggegator

This Django Project runs a news aggegator available at [neuesvomtage.de](https://neuesvomtage.de). The code is licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) as stated in the LICENSE.txt file. 

This source code comes with a minimal example set of demo data, which can be inserted into a database to get started.

### Getting Started - Docker Compose

To run the project in a docker compose environment, all you need is an installed [Docker engine](https://www.docker.com/) or Docker Desktop, and the docker-compose package.

```shell
$ docker compose up
$ docker compose exec web /venv/bin/python manage.py loaddata contrib/demo_data.json
$ docker compose exec web /venv/bin/python manage.py update_feeds
$ docker compose exec web /venv/bin/python manage.py update_icons
$ docker compose exec web /venv/bin/python manage.py generate_top_words
```

Note that the configuration in the .env.docker file contains only example values and enables DEBUG mode, among other things. The values should be adjusted for a public site.

### Create an admin User

This command creates an admin user. The admin interface is available at [http://localhost:8000/admin](http://localhost:8000/admin).

```shell
$ docker-compose exec web venv/bin/python manage.py createsuperuser
```
