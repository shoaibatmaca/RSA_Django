# How to implement the rsa in the django project

Hey! Hope you're doing great.  
Below is a **complete hands-on guide** on how to implement the rsa

```bash
pip i djangorestframework djangorestframework_simplejwt pycryptodome cryptography
# For generating .pem
```

```bash
iska faida ye hoga k ye monolithic/ microservice m used by default jwt hs256 - a symmetric algo that is fast but the same secret key is uses between the all micro service for signin or verifity token so that here is a chance to stolen and forge the oken
but in the rsa 256  uses a asymmetric algo that means one private key from the server side like auth and the second one is the public key server signup user using the private key and the token from here and the other service verify it using the public key not to direct access the private key
it is most commonly used approach for secure https of ur confidentail data, privacy
```

```bash
pip install django-jazzmin
and go to the setting file and added it into the top at installed app
```
