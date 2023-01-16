![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=12&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=Done&color=green&style=for-the-badge)

# ocrp12.1

Develop a Secure Back-End Architecture Using Django ORM  
⭐ New version ⭐

![Logo epicevents](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/epicevents.png "Logo")


****
### Description
The project purpose is to create an API with the [Django REST framework](https://www.django-rest-framework.org) and a 
[PostgreSQL](https://www.postgresql.org) database.  
Epic Events is a company which specialises in events organisation and needs a new customer relationship management software.  

This API allows users to :

- Create users
- Assign user permissions
- Create customers / contracts / events
- Update these according to the user's permissions
- Use the django admin interface (only for managers)

All endpoints are explained in the Postman documentation :  

[![Logo PostMan](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/postman.png "Postman")](https://documenter.getpostman.com/view/19051270/2s8YzXwLV1)

****
### Installation

Open your terminal and navigate to the folder where you want to install the API.  
Then, clone this repository :

    git clone https://github.com/FLinguenheld/ocrp12.1

Navigate into the *ocrp12.1/* folder and create a virtual environment :

    python -m venv env

Activate it :

    source env/bin/activate

Necessary packages are listed in the file *requirement.txt*.  
Install them :

    pip install -r requirement.txt


#### Database

This application uses [postgresql](https://www.postgresql.org). You have to install it according to your distribution, then 
create a database and a user with this information :

    database name : epic_events
    user : epic_user
    user password : 01234

Django will search the database on *localhost* with the port *5432*.  
You can change this behaviour in the settings file.

Here an example to create or delete a database :

    sudo -u postgres psql
    create database epic_events;
    drop database epic_events;

#### Permissions

Once the first migration is done, groups **manager** and **sales** are automatically added.  

💡 To create a manager, create a new user, check the box *staff* and add the group *manager*.  
You can also use the endpoint 'users' (see the [Postman documentation](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/postman.png) for more details)


- manager :  
All staff users can open the admin panel (with restricted actions) and due to being in the manager group, they can manipulate data.  
Staff users also have a write access on all endpoints.  

- sales :  
All users in this group are authorised to create a new customer.  

****
### Launch

Navigate into the *ocrp12.1/* folder and activate the virtual environment.  
Launch the server with the command :

    python manage.py runserver

Then, you can use your browser, Postman or your terminal.

    http://localhost:8000/

Django administration is automatically activated, so you can create a superuser and open it with the link :  
http://localhost:8000/admin/

    python manage.py createsuperuser

****
### Testing

This code uses the framework [pytest](https://docs.pytest.org/en/latest/contents.html) and the plugin [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) to test endpoints.  
To launch a new test, open a terminal, navigate into the root folder and activate the virtual environment.  
Then launch the command :

    pytest -v

****
### Diagram

![Epic crm diagram](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/Diagram_Epic_events.png "Logo")

****
### Bonus

To easily add several database entries, you can use the fantastic file **postman_init.py**.  
💡 You need manager or superuser credentials.

Launch the server in a terminal. Then open a new one, navigate into the root folder and use the command :

    python postman_init.py --username <admin> --password <admin01234>

It will create several users (with the pass *test01234*), customers, contracts and events.
