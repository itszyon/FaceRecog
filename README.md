# FaceFinder
#### Video Demo: 
#### Description: (explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them)

FaceFinder is a web page that organises your photos into diferent folders using facial recognition. It takes in images of faces the user wants to identify in the images and sorts them by name with the help of the python library called face-recognition.

Usage:
First create your own account to have access to the page. This username will be used to name the folder created on your computer. Once in the index you can add faces for the software to identify. After this, there is a section where you can upload your photos to be organised. At any point, you can have a look at the photos you have uploaded to the page in their corresponding folders by clicking View Gallery and ticking the person you want to see.

This version of the page only works locally on your own computer due to the fact that it works directly on folders. Data bases could be used to upscale the scope of the web page.

The web page is made using the Flask libraries which means we need an app.py file, a templates folder and a static folder.

The python file takes care of the backend of the page. It contains 8 different routes:

"/" (hompage): this routes' only purpose is to render the hompage html file.

"/login": in this section I had to be careful with the user that was logging in. First of all I had to check if the username introduced matches with the password using an SQL database. After this I have to make sure that all folders are available to this user; that is to check if the data folder exists and that the user has their own folder assigned to their username with the necesary folders in it. They need a folder called faces to store images of the faces they want identify and a folder called gallery to store the photos they want to organise. A problem I encountered in this seccion was the fact that empty folders dissapear when you stop running VS, so I have to make sure that the folders exist every time the user logs in.

"/logout": the only thing it does is clear the session currently in use.

"/register": this route takes in the username and password introduced by the user in the html file. I have to check that the inputs have not been left blank and that the username is not already in use. As I did with the log in route, I have to create all the new folders for the user to use. I decided not to have password requirement since the web page can only be used locally and security is not the main purpouse.

"/index": this is the main route when a user logs in. The app.py file sends the directories of the images that the user has inputed as faces to display them in an html file.

"/addfaces": the user can use this directory to upload images of faces they want the software to identify. When an image is submited, it is read and written into a new file. This file is then stored in the 'faces' folder of the user who is logged in. Aparrt from this, a new folder is created insde the 'gallery' folder with the name of the image provided (recommend the user to sumbit image with the persons' name)

"/organisephotos": this route fulfills the main purpouse of the web page. It is in charge of organising the images inputed into the folders of the faces the user provides. The first step it takes is to store the image uploaded in the main folder of the users' gallery called 'full_gallery'. Apart from this, it runs the image through the face-recognition library to check if there is somenone to recognise. If the code recognises more than one person in the image, it will store it in the folders of everyone who is in it. A small, but important, detail to take into account is the fact that a user could input an image with no faces in it (for example a landscape or a vehicle). To solve the possible problem this can cause, I have to check if there is a face before saving the face enconding. A new version of the web page would permit the user introduce various images at the same time to organise them quicker.

"/viewgallery": here the user is able to view the images they have uploaded to the page. There is a dropdown select menu that gives the user the chance to view only the images of the person they have selected.

In the 'templates' folder are all the html filess necesary to display the web page on the screen. I decided to go with a simple (somewhat minimal) colourful design, mainly using the colors of the logo and simple shapes, like squares and circles. There are three main layouts I have followed to design the rest of the files: 'apology.html', 'layout_profile.html' and 'layout.html'. 'apology.html' is a bit special because it is only used to inform the user of errors that have occured. 'layout_profile.html' is used to build the login and register files and 'layout.html' to have the same structure in all the files when the user is logged in.

An issue I had with the html templates was with the image file inputs in 'addfaces.html' and 'organisephotos.html'. The problem was that I didn't know how to send the file from the html file to the python file and save it. Finally, I ended up using the request.files() function and writting the inputs in files created in python. It may not be the fastest way to do this but it is the best solution I could find. Another limitation with this solution is the fact that it is not possible to distinguish when an images starts and ends if various images are inputed.