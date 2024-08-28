# Messimtger

![logoBig.png](static%2FlogoBig.png)

## Setup the project

Python modules :
flask
flask-sqlalchemy

In a terminal :
```bash
 pip install flask, flask-sqlalchemy
 ```
## Populate the database [optional]
You can edit the `"database/populate_database.py"` script to create a pre-existing layout with multiple registered users, messages etc...
By default, the database reset at startup but you can disable this by going to `"database/database.py"` and remove the line  `db.dropall()`.

## Run the Flask server

To run the server, you simply have to run the `app.py` main script
```bash
python3 app.py
 ```

It is still possible to run it as standard flask app if needed :
```bash
flask app.py run
 ```

## Project Structure
The specificity of the project comparing to a standard flask app is the image upload feature. 
The uploaded images are saved in the `database/image_database` directory with a unique name.
The database containing all of the other informations (Users, Conversations, Messages) is located in `database/database.db`.

The user interface uses as much bootstrap component as possible to keep it responsive and mobile-friendly.

### Detailed Structure
```
MessimtgerServer
│   app.py
│   README.md
│   session_manager.py
│
├───database
│   │   database.db
│   │   database.py
│   │   models.py
│   │   populate_database.py
│   │
│   └───image_database
│           ExampleImageUpload.jpg
│
├───static
│   │   logo1.png
│   │   logoBig.png
│   │
│   └───css
│           style.css
│
└───templates
        base_template.html.jinja2
        contact.html.jinja2
        dashboard.html.jinja2
        home.html.jinja2
        index.html.jinja2
        login.html.jinja2
        navbar.html.jinja2
        register.html.jinja2
```