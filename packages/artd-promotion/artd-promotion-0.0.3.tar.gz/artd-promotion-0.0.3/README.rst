=====
ArtD Promotion
=====
Art promotion is a package that makes it possible to manage promotions and rules based on customers, categories and products.
Quick start
-----------
1. Add to your INSTALLED_APPS setting like this::
INSTALLED_APPS = [
        ...
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_customer'
        'artd_product',
        'artd_promotion',
    ]
2. Run `python manage.py migrate` to create the models.