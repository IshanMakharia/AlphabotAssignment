# AlphabotAssignment

# A full-stack web application built using flask-python and SQLite


# How to run commands :

  1. Setup local environment and install all other dependencies 
  
        sh ./localsetup1.sh
        
        
  2. Then start the application : 
  
        sh ./localrun.sh 
        



# API routes :

1. GET  / : Redirects to homepage.

2. GET, POST  /login : For opening login page and maintaining login session for user.

3. GET, POST  /signup : Registration for first time users.

4. GET  /logout : For ending the login session.

5. GET  /notes/getAll : For retrieving all the notes of a particular user.

6. GET, POST  /notes/add : For creating an new note.

7. GET  /notes/get/<int:id> : For fetching a single note by id.

8. GET, DELETE  /notes/delete/<int:id> : For deleting a note by id.

9. GET, PUT /notes/update/<int:id> : For updating an existing note.
