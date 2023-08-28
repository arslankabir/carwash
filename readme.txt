>> Install PYTHON 3.9.1
>> CREATE A FOLDER OF THE PROJECT AND NAME IT ANYTHING e.g. car_washer
>> put the unzipped folder of the project in it.
>> open it in VS code or any code editer you like
>> use terminal and the path of that project

Run commands one by one
>> pip install virtualenv
>> virtualenv cwenv
>> cwenv\Scripts\activate
>> pip install requirements.txt

if you dont want to use the database that is already exist then delete the database file and run commands
>> python manage.py makemigrations 
>> python manage.py migrate

To run the project
>> python manage.py runserver

Superuser admin
>>admin user name: admin
>>admin password:  admin