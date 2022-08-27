# TruBoard
Web Forum or Discussion Board

TruBoard is web discussion forum developed using:

* python(Django) as the backend of this project for mapping and routing urls, interacting with the database, 
* HTML, 
* CSS(bootsrap) for styling, 
* JavaScript(Popper.js, simplemde.js): popper.js for displaying a dropdown menu for authenticated user, simplemde.js for adding a markdown editor to text areas

## New boards can only be created by an Admin

### Unauthenticated user can:
1. view discussion boards
2. view topics associated with each board
3. view Posts associated with each topic

### Authenticated users have all the capabilities of unauthenticated user plus:
1. create a new topic
2. create a new post
3. Edit their posts
