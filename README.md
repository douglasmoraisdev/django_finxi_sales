# Asynchronous File Processor using Django and Celery

This app asynchronously process sale files (.xlsx Excel extension). Insert the records on Database and notify the user (front-end) when finish.

## Requirements
- Docker: 
    https://docs.docker.com/install/

- Docker Compose:
    https://docs.docker.com/compose/install/


## Running Instructions

1. Clone the project locally:

```sh
$ git clone git@github.com:douglasmoraisdev/django_finxi_sales.git
```

2. Run docker-compose in project dir
```sh
$ cd django_finxi_sales/
$ docker-compose up
```

3. Open the Dashboard on browser using the url:
```url
http://localhost:8000/dashboard/
```

*Done.*

### Extras: 

- (Optional) Create a superuser, for Django admin usage

```sh
$ docker exec -it <docker_finxi_web_container_id> python manage.py createsuperuser
```
Django Admin url:
```url
http://localhost:8000/admin/
```
