# "EzPlanner" Portfolio Management Fullstack Application

### Live Demo

https://youtu.be/p0GuMR8rphQ

## About

This reactive, web application uses the yFinance API to get up-to-date prices on stocks and updates the value of your portfolio accordingly, as well as tracking transactions you have made.

## Technology

This application was built with a RESTful API backend using Django, that uses a MySQL database for data storage and ont he frontend uses Angular and TypeScript to create a simple portfolio manager.

## Run Locally

Clone the repository. You will first need to set up a local MySQL database. Then follow these steps to connect it to the API. Run the following commands in the root of this repo.

1. `virtualEnv\Scripts\activate`
2. `cd PortfolioManagmentAPI`
3. `django-admin startproject MySQL`

Now open `MySQL/settings.py`. Inside of the `DATABASES` variable, using the name of the databse you created, user and password, ensure this is filled out

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<DB_NAME>', # Enter your DB name
        'USER': '<ROOT_USER>', # The name is likely "root"
        'PASSWORD': '<ROOT_USER_PASSWORD>', # Whatever you set the root password to
        'HOST':'localhost',
        'PORT':'3306',
    }
}
```

Finally, you can follow these commands to initialize the database and run the project. Start at the root folder of the repo.

1. (If you have not already activated the virtual environment) `virtualEnv\Scripts\activate`
2. `cd PortfolioManagementAPI`
3. `python manage.py migrate`
4. `python manage.py makemigrations`
5. `python manage.py runserver`

Now in a new terminal, starting again at the root of this repository:

1. `cd frontend`
2. `ng serve`

Then, navigate to `http://localhost:4200/` to view the development version of this project.
