# Voucher Wheel

![alt text](sell-page/screenshot1.png "Voucher Wheel")


Voucher Wheel is a powerful tool to engage your customers by giving them a chance to win a prize by spinning a lucky wheel.

Developed in Python, Django and Javascript, Voucher Wheel is fully customisable in an admin portal.

The wheel was made in Scalable Vector Graphics (SVG) making the website fully responsive and flexible for your needs.

Voucher Wheel can be used as a stand-alone Squeeze Page or Landing Page to capture emails and build a newsletter list. Or as a plugin or popup to your website!

- Product page: https://codecanyon.net/item/voucher-wheel-engage-and-give-prizes-to-your-customers/33951156
- Live Demo: https://voucher-wheel.visiansystems.com

## Requirements

- Must have pip, Python 3 and Django installed
- Install `virtualenv`.
    - Virtualenv is a tool to create such environments. You can install it by using pip:
        
        ```bash
        pip install virtualenv
        ```
    
## ****Getting started****

1. First, you need to set up your virtual environment on the project's root directory:

```bash
virtualenv venv
source venv/bin/activate
```

2. Then go to the `wheel` folder and run the following commands:

```bash
pip install -r requirements.txt
python manage.py migrate
```

3. Now, create the admin user:

```bash
python manage.py createsuperuser
```

4. Create the static files:

```bash
python manage.py collectstatic
```

5. Load the initial data:

```bash
python manage.py loaddata prizes
```

6. Finally, run the application:

```bash
python manage.py runserver 0.0.0.0:8000
```
