<div align="center">

# Horus👨‍🔧🚘

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](./README.es.md)


Horus is the base name for this project, which is a web application to control sales of spare parts and services for a mechanical workshop.

It was required by a small workshop which wanted to control the flow of income, as well as the inventory of the products or spare parts they used in each service.

![dashboard](./imgs/dashboard.png)

Visit the test [website](https://xtestuser.pythonanywhere.com/) to know more.
Use this credentials: username: **admin** password: **abc123/-**
</div>


## 📖 Installation
#### Download this repository

> It is recommended to use a virtual environment for the installation of dependencies..!

- virtualenwrapper
```bash
mkvirtualenv (name env)
```

- virtualenv/venv
```bash
python -m venv (name env)
```
> Activation of the virtual environment
- virtualenwrapper
```bash
workon (name env)
```

- virtualenv/venv
```bash
(name env)\Scripts\activate
```

> **Installing the dependencies**
To install the dependencies, you must locate them at the **requirements.txt** file level and run the following command:
```bash
pip install -r requirements.txt
```
#### Create a new user

#### Run the server and launch 🚀 the web application 💻
> To set up the server we must be at the level of the **manage.py** file
```bash
python manage.py runserver
```

If everything worked correctly it should show that the application is running showing the address and port.
<img src="/imgs/runserver.png" style="border-radius:5px">

## ⚙️ Basic use of the web application

## 🛠️ Stack
* ![Python Logo](https://www.python.org/static/img/python-logo.png){height=36px}- A programming language that lets you work quickly and integrate systems more effectively.
* ![Django Logo](https://www.djangoproject.com/m/img/logos/django-logo-negative.png){height=36px} - Makes it easier to build better web apps more quickly and with less code
* ![Django Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/JavaScript-logo.png/768px-JavaScript-logo.png){height=36px} - Interpreted programming language, a dialect of the ECMAScript.
* ![Django Logo](https://cdn.icon-icons.com/icons2/2415/PNG/512/postgresql_original_wordmark_logo_icon_146392.png){height=36px} - Object-oriented relational database management system
