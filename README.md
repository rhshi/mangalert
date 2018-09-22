# mangalert
Alert system for manga updates

## Requirements
* Python 3.6.x
* Flask and various Flask extensions (Flask-Alchemy, Flask-Login, etc.)
* BeautifulSoup

## Description
* Followed Miguel Grinberg's [tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) for a general guide on how to set up and organize a Flask app.  This runs on a simple SQLite databse store on disk.  All scripts in [`app.src`](https://github.com/rhshi/mangalert/tree/master/app/src) are my own, which include the gathering of manga follows and updates.
* The goal here was to create a website (and possibly in the future when I have more time, an app) to alert users, through email and through other means (like Twitter direct messages), whenever there was an update to a manga that the user was following.  I implemented a method through which the user could connect their MangaDex MDList (example [here](https://mangadex.org/list/4680)), and then the website would then parse through all the follows, determine ongoing and completed series, and add the information to the database using a many-to-many relationship structure.

## Future work
A few things impeded me from allowing the website to reach its intended vision.  One was the nature of the SQLite database, which kept throwing I/O errors when parsing the MDLists (issue explained [here](https://stackoverflow.com/questions/9017762/what-is-the-maximum-connections-for-sqlite3-database/9018525#9018525)); in order to move forward, I would have had to deploy the website and use a different database.  I didn't want to deploy at this point in time (don't know whether to use Docker or some other method), so I had to end progress here.  One thing I want to add is a recommendation system for users located on the "explore" page using Spotlight that allows users to find the manga best suited for them.
