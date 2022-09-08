# FaceFinder
#### Video Demo: 
#### Description: (explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them)

FaceFinder is a web page that organises your photos into diferent folders using facial recognition. It takes in images of faces the user wants to identify in the images and sorts them by name with the help of the python library called face-recognition.

Usage:
First create your own account to have access to the page. This username will be used to name the folder created on your computer. Once in the index you can add faces for the software to identify. After this, there is a seccion where you can upload your photos to be organised. At any point, you can have a look at the photos you have uploaded to the page in their corresponding folders by clicking View Gallery and ticking the person you want to see.

This version of the page only works locally on your own computer due to the fact that it works directly on folders. Data bases could be used to upscale the scope of the web page.

The web page is made using the Flask libraries which means we need an app.py file, a templates folder and a static folder.

The python file takes care of the backend of the page. It contains 8 different routes:

"/" (hompage): this routes' only purpose is to render the hompage html file.

"/login": in this section I had to be careful with the user that was logging in. First of all I had to check if the username introduced matches with the password using an SQL database. After this I have to make sure that all folders are available to this user; that is to check if the data folder exists and that the user has their own folder assigned to their username with the necesary folders in it. They need a folder called faces to store images of the faces they want identify and a folder called gallery to store the photos they want to organise. A problem I encountered in this seccion was the fact that empty folders dissapear when you stop running VS, so I have to make sure that the folders exist every time the user logs in.

"/logout": the only thing it does is clear the session currently in use.

"/register": this route takes in the username and password introduced by the user in the html file. I have to check that the inputs have not been left blank and that the username is not already in use. As I did with the log in route, I have to create all the new folders for the user to use.

"/index": 