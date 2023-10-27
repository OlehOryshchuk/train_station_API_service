## Train Station API Service

![Django](https://img.shields.io/badge/Django-4.2.6-brightgreen.svg)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.14-blue.svg)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2.22.0-brightgreen.svg)

Train Station API Service is a web application built with Django REST Framework offering a platform
for managing and accessing data related to train stations, It provides APIs for various functionalities
like creating, listing, filtering, searching, and managing train stations, trips, orders.

## Features
* Unauthenticated users can't do anything
* Authenticated users can list and retrieve resource, except user can create order and ticket
* Superuser (admin, staff) can create every resource, list and retrieve
* Secure authenticated system. Train Station API provides registration anda JWT
    (JSON Web Token) authentications. Users register then login for obtaining JWT
    access token to authenticate themselves and refresh token for refreshing access
    token when it is expired
* Users can filter trains by train type and search by it's name
* Users can filter trips by train and trip route
* Users can filter ordered tickets by trip route
    and ordering orders in ascending and descending order
* API documentation 
* Admin panel /admin/

## Installation
1. Clone git repository to your local machine:
```
    git clone https://github.com/OlehOryshchuk/train_station_API_service.git
```
2. Copy the `.env.sample` file to `.env` and configure the environment variables
```
    cp .env.sample .env
```
3. Run command. Docker should be installed:
```
    docker-compose up --build
```
4. Access API as superuser you can use the following admin user account:

- **Email** train@gmail.com
- **Password** train_rvt_27

It is recommended to create your own user accounts fot production use.

### Usage
To access the API, navigate to http://localhost:8000/api/ in your web browser and enter one of endpoints.

### Endpoints
Train Station API endpoints 
- `/train_station/stations/`
- `/train_station/train_types/`
- `/train_station/crews/`
- `/train_station/trains/`
- `/train_station/orders/`
- `/station/routes/`
- `/train_station/trips/`

User API endpoints:
- `/user/register/`
- `/user/token/`
- `/user/token/refresh/`
- `/user/token/verify/`

Admin (superuser) endpoint:
- `/admin/`

Documentation:

- `/doc/swagger/`: To access the API documentation, you can visit the interactive Swagger UI.
