# library-application

This is a library application that is built with [Flask](http://flask.pocoo.org/) for [python](http://python.org).
This is an application that manages the list of users and books in the library.

## Features
- This application allows user to signup/login. 
- As a logged in user, you can see a list of books that are stored in the library.
- As a logged in user, you can borrow a book from the library.
- As an Admin, you can add books, remove books, add quantities to book, categorize books.

## Tools
- virtualenv (virtual environment)
- Flask (framework)
- SqlAlchemy(ORM)
- Sqlite(database)
- Ajax
- Social Auth (Auth0)

## Installation
To install the application, take the following steps

1. enter the following command in the command prompt to install the virtual environment
```
pip install virtualenv
```
2. create a folder and change directory to that folder on the command prompt
3. enter the command below to install the virtual environment in that folder
```
virtualenv "app name"
```
4. activate the virtual environment to start running
```
"app name"\Scripts\activate
```
5. Install flask into the project directory
```
pip install flask
```
6. Install all dependencies found in the requirements.txt file
7. To run the application, enter the command below in the command prompt
```
python run.python
```

Feel free to give me feedback on areas you feel needs to be worked on.