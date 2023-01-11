![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=12&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=InProgress&color=blue&style=for-the-badge)

# ocrp12.1

Develop a Secure Back-End Architecture Using Django ORM  
⭐ New version ⭐

![Logo epicevents](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/epicevents.png "Logo")


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

This application uses [postgresql](https://www.postgresql.org). You have to install it according to your distribution then 
create a dabase and an user with this information :

    database name : epic_events
    user : epic_user
    user password : 01234

Django will search the database on *localhost* with the port *5432*.  
You can change this behaviour in the settings files.

Here an example to create or delete a database :

    sudo -u postgres psql
    create database epic_events;
    drop database epic_events;

#### Permissions

Once the first migration is done, groups *manager* and *sales* are automatically added.  
💡 To create a manager, create a new user, check the box *staff* and add the group *manager*.  

- manager :  
All staff users can open the admin panel (with restricted actions) and due to the manager group, they can manipulate data.  
Staff users also have a write access on all endpoints.  

- sales :  
All users in this group are authorized to create a new customer.  
Superuser and staff (managers) are allowed to add or remove users of this group.  

****
### Launch

Navigate into the *ocrp12.1/* folder and activate the virtual environment.  
Launch the server with the command :

    python manage.py runserver

Then, you can use your browser, Postman or your terminal as well.

    http://localhost:8000/

Django administration is activated, you can create a superuser and open it with the link :  
http://localhost:8000/admin/

    python manage.py createsuperuser

****
### Documentation

All endpoints are explained in the Postman documentation :  

[![Logo PostMan](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/postman.png "Postman")](https://documenter.getpostman.com/view/19051270/2s8YzXwLV1)

****
### Testing

This code used the framework [pytest](https://docs.pytest.org/en/latest/contents.html) and the plugin [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) to test endpoints.  
To launch a new test, open a terminal, navigate into the root folder and activate the virtual environment.  
Then launch the command :

    pytest -v

****
### Diagram

![Epic crm diagram](https://raw.githubusercontent.com/FLinguenheld/ocrp12.1/main/logos/Diagram_Epic_events.png "Logo")
