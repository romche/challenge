############
Users
############

API for register user, getting token as well as for refreshing and for rekoking.
Using (Django OAuth Toolkit) and Authorization grant type: Resource owner password-based


Endpoints for testing
=====================
* POST /authentication/register/        {"username": "username", "password": "1234abcd"}
* POST /authentication/token/           {"username": "username", "password": "1234abcd"}
* POST /authentication/token/refresh/   {"refresh_token": "<token>"}
* POST /authentication/token/revoke/    {"token": "<token>"}
