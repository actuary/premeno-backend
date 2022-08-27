# Mascot

MHT Risk Assessment Tool

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Workflow Build](https://github.com/actuary/premeno-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/actuary/premeno-backend/actions/workflows/ci.yml)
### About
https://premeno-frontend.herokuapp.com/about

MAsCoT has been built to communicate the risks and benefits of taking menopausal hormone therapy (MHT), also known as
hormone replacement therapy (HRT). It's aimed at women who are experiencing menopausal symptoms and are considering
their options. It is not intended to replace the advice of a doctor, it is instead intended to facilitate shared
decision making between a doctor and their patient.

This is the repository from the backend of the Mascot app. The frontend can be found
[here](https://github.com/actuary/premeno-frontend). The backend provides a service (built using the Django REST
framework) which calculates risks and sends back reports to the frontend application. This
backend can be deployed separately as a standalone API.

Currently, only breast cancer risk is considered, and the hope is to expand to other risks (upside risks as well as
downside risks). The breast cancer risk can be calculated one of two ways, using a modified Gail model, or using
the CanRisk tool. As this is only a pilot project, we don't make any statements about the accuracy of such models,
however, we hope to be able to do so in future versions.

The tool is built using Django and Postgres with a responsive React front-end.

### Acknowledgements
This tool can make use of the CanRisk tool web-services ([canrisk.org](https://www.canrisk.org/about/)). The CanRisk tool is supported by grant PPRPGM-Nov20\100002 from
Cancer Research UK. Citations are below:

[1] Carver, Tim et al. "CanRisk Tool-A Web Interface for the Prediction of Breast and Ovarian Cancer Risk and the Likelihood of Carrying Genetic Pathogenic Variants." Cancer epidemiology, biomarkers & prevention : a publication of the American Association for Cancer Research, cosponsored by the American Society of Preventive Oncology vol. 30,3 (2021): 469-473. doi:10.1158/1055-9965.EPI-20-1319
[2] Lee, Andrew et al. "BOADICEA: a comprehensive breast cancer risk prediction model incorporating genetic and
nongenetic risk factors" Genetics in Medicine, Volume 21, Issue 8, 1708 - 1718
[3] Archer S, Babb de Villiers C, Scheibl F, Carver T, Hartley S, et al. (2020) Evaluating clinician acceptability of the prototype CanRisk tool for predicting risk of breast and ovarian cancer: A multi-methods study. PLOS ONE 15(3): e0229999. https://doi.org/10.1371/journal.pone.0229999


## Deployment
### Dependencies

The project has the following dependencies:
-   Python 3.9+
-   wkhtmltopdf
-   Postgres 12

The front-end has the following depenencies
-   Built with React 18.2.0+
-   Modules specified in the package.json

### Deploying locally without Docker

To deploy locally without Docker, first install the dependencies above.

Then download the projects and their dependencies
```
git clone https://github.com/actuary/premeno-backend.git backend
git clone https://github.com/actuary/premeno-backend.git frontend
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements/local.txt
```

For the backend, create a .env file in the backend folder, and inside store the following variables
```
DATABASE_URL='<POSTGRES DB URL>'
CANRISK_API_USER='<Canrisk username>'
CANRISK_API_PSWD='<Canrisk password>'
```

Start the backend service:
```
cd backend/
export DJANGO_READ_DOT_ENV_FILE=True
python manage.py runserver
```

Create a superuser:
```
python manage.py createsuperuser
```

For the frontend, create a .env file in the frontend folder, and inside store the following variables
```
REACT_APP_API_USER='<admin user>'
REACT_APP_API_PSWD='<admin password>'
REACT_APP_API_URL='http://127.0.0.1:8000'
```

Start the front-end component
```
cd ../frontend/
npm start
```

Navigate to http:/127.0.0.1:3000

### Deploying locally with Docker
Alternatively, if you want to use Docker. This requires docker and docker-compose

Clone the repos
```
git clone https://github.com/actuary/premeno-backend.git backend
git clone https://github.com/actuary/premeno-backend.git frontend
```

#### docker-compose file

Can use the following docker-compose file, saved as say, `local.yml` in the parent directory where backend/ and
frontend/ are stored.
```
version: '3'

volumes:
  premeno_local_postgres_data: {}
  premeno_local_postgres_data_backups: {}

services:
  django:
    build:
      context: ./backend/
      dockerfile: ./compose/local/django/Dockerfile
    image: premeno_local_django
    container_name: premeno_local_django
    platform: linux/x86_64
    depends_on:
      - postgres
    volumes:
      - ./backend:/app:z
    env_file:
      - ./.envs/.local/.django
      - ./.envs/.local/.postgres
    ports:
      - "8000:8000"
    command: /start

  frontend:
    build:
      context: ./frontend/
      dockerfile: ./compose/local/frontend/Dockerfile
    image: premeno_local_frontend
    container_name: premeno_local_frontend
    platform: linux/x86_64
    env_file:
      - ./.envs/.local/.frontend
    ports:
      - "3000:3000"
    restart: always
    stdin_open: true
    command : npm start

  postgres:
    build:
      context: ./backend/
      dockerfile: ./compose/production/postgres/Dockerfile
    image: premeno_production_postgres
    container_name: premeno_local_postgres
    volumes:
      - premeno_local_postgres_data:/var/lib/postgresql/data:Z
      - premeno_local_postgres_data_backups:/backups:z
    env_file:
      - ./.envs/.local/.postgres

  docs:
    image: premeno_local_docs
    container_name: premeno_local_docs
    platform: linux/x86_64
    build:
      context: ./backend/
      dockerfile: ./compose/local/docs/Dockerfile
    env_file:
      - ./.envs/.local/.django
    volumes:
      - ./backend/docs:/docs:z
      - ./backend/config:/app/config:z
      - ./backend:/app/premeno:z
    ports:
      - "9000:9000"
    command: /start-docs
```

#### Environment variable files
Make a .envs directory
```
mkdir .envs/.local
```

Add a `.envs/.local/.postgres` file with the following entries
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=premeno
POSTGRES_USER=<some username>
POSTGRES_PASSWORD=<some secure password>
```

Inside `.envs/.local` put a .django environment file, a .frontend file with the details as in the .env files without
Docker. For the DATABASE_URL in .django, use the details in .postgres

#### Composing
Build and then run the containers

```
docker-compose -f local.yml build
docker-compose -f local.yml up
```

You can create a superuser for Django (as in the .frontend file), by exec'ing into the container (only needed the first
time the postgres db is created).
```
sudo docker exec -ti premeno_local_django /bin/bash
root@4314e3413d:/app# python manage.py createsuperuser
```

### Heroku
This tool can be readily deployed to heroku. Follow the steps in the [cookiecutter docs](https://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).
You will also need the [wkhtmltopdf buildpack](https://github.com/dscout/wkhtmltopdf-buildpack), and to set an
environment variable WKHTMLTOPDF=/app/bin/wkhtmltopdf

### Test coverage

Tests and coverage can be run:
```
$ coverage run -m pytest
$ coverage html
$ google-chrome htmlcov/index.html
```
