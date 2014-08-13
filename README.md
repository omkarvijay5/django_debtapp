django_debtapp
==============

Debtapp is a web application through which user can share their expenses between friends.
It also let users know how much amount they owe to their friends or how much amount their friends owe the user

To quickly try it locally follow the below steps
    1.Installing virtual environment
       virtualenv venv
       source venv/bin/activate/
    2. Installing debtapp
        cd django_debtapp
        pip install -r requirements.txt
        python manage.py syncdb
    3. Adding environment variables
        export EMAIL_HOST_USER='your_valid_working_email'
        export EMAIL_HOST_PASSWORD='your password'
        export SECRET_KEY='secret key'

    python manage.py runserver or
    python manage.py runserver --settings=django_debtapp.settings.local

    By following the above steps you will be able to access http://localhost:8000/accounts/register/ which enables you to register in the app