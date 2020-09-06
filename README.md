# Welcome to [Bottleneck](https://bottleneck-gaming.herokuapp.com/?page=1)

![Bottleneck Responsive](static/img/ReadME/responsive.jpg)


## Introduction
[Bottleneck](https://bottleneck-gaming.herokuapp.com/) is a open videogame based website, where you can just signup and you are ready to write your posts, also if you just want to read what the community is posting, you are not required to login.

This proyect is a little reflects a part of mine, the side that likes the videogames despite the lack of time to enjoy this hobby nowadays.

___


## Table of Contents
2. [Project's Purpose](#projects-purpose)
3. [UX](#ux)
4. [Wireframes](#wariframes)
5. [Features](#features)
    - [Existing Features](#existing-features)
    - [Future Features](#future-features)
6. [Data Integration](#date-integration)
7. [Technologies used on the project](#technologies-used-on-the-project)
    - [Front-End](#front-end)
        - [HTML](#html)
        - [CSS](#css)
        - [Bootstrap](#bootstrap)
    - [Back-end](#back-end)
        - [Python](#python)
        - [Flask](#flask)
        - [Jinja2](#jinja2)
        - [PyMongo](#pymongo)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Credits](#credits)
11. [](#)
12. [](#)
13. [](#)
14. [](#)

___

## Project's Purpose
The project pretend to show all the learned during the module. Showign the hability to use [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) to connect with the back-end and display the data required or edit it.


____

## UX

## Wireframes

## Features
### Existing Features
<u>**Landing Page**</u></br>
- Navbar
- Posts
- Pagination
- Footer

<u>Navbar</u></br>
Thanks to <i>bootstrap</i> the <i>navbar</i> is responsive, fully functional and developed quickly.
For some screen sizes __CSS__ was required with help of the __media queries__.

<u>Pots</u></br>
The post are being displayed through a jinja for loop, depending on the offset and the limit prestablished in the backend program, this data only will four posts per pagination page, which each pagination page will be displayed at the end of the four post.

<u>Pagination</u></br>
in order to develop the pagination section, some research was needed to understand how it works and what id does. Lots or reading and some hlep from the man behind [Pretty Printed's](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ) [YouTube](https://www.youtube.com/) channel, despite all the tools and techniques, this was the only way I could undertand the best to then inplement it to Flask to pass it to Jinja.

The pagination section has prev as previous page, next to go to the next page and the numbers which depending on the number of posts stored in the database where every four posts will count as a paginated page.

<u>Footer</u></br>
The footer displays **bottleneck's** links to <i>github</i> and to <i>heroku's</i> app under **"MileStone Project 3"** section and under **"Made by"** section only displays my name, <i>Jose Enciso</i>.

<u>**New Post**</u></br>
The new post site will guide the user trough to at the end publish the post. In here the user will find a review section where the user will be able to use <i>HTML</i> tags to add more visuals. This <i>HTML</i> feature is not supported on pros and cons section.

Each game has a date release and a pegi rate, as what audience is the game for as what kind of content the game has and what platforms it will be released.

The user will be asked to choose six images, one will be used as a cover and the other five as part of the carousel. Due to the nature of the way bootstrap manage the input files it doesn't display what file has been updated.

<u>**Edit post**</u></br>
The edit post is basically the same as the new post site. The difference is that it shows the previuos stored information in the database and can be changed depeding the needs.

this edit post site, shows who made the post and when. The images section is different from the new post site,  The images section visually is different, with the purpose of making easy the display the previous images and file to be changed.

<u>**Register & Login**</u></br>
The register and login are tow simple forms where to resgister and login in case there is a user who would like to edit or create a new post.

<u>**User**</u></br>
The user site will display the a table with the post created by the user, displaying title, sub-title and date posted.


## Data Integration
PyMongo is the driver used to stored data into the collections in MongoDB, the collections are posts and users. In posts collections will be stored each post created and in the users collections will store each new user created.

The images will be stored in three different collections, in the first one is the posts, creating the relationship with the name, fs.files will store the images details and the fs.chuncks will sotred the image in doded in string.

## Technologies used on the project
* **Front-End**
    - HTML
    - Bootstrap
    - CSS
    ___
    As we all know Html was used to <u>structure</u> the website while ***bootstrap*** helped a lot to get some things done faster, such as the **navbar**, **gallery** which was achieved with the ***carousel***, and other just to style, in certain ocasions ***CSS*** was needed to complete what was out of bootstrap scopes or to fix some of the issues that ***cols*** and ***rows*** where happening due to their nature. Also some components needed to be discarded to used pure __CSS__ due to the needs of the some parts of the project.
    ___
* **Back-End**
    * Python
    * Flask
    * Jinja2
    * PyMongo
    ___
    This project was a challange, as it required a lot os researching, finding multiple solutions but to find the right one, the one that suited the problem in that moment was a time consuming.
    ___

## Testing
The testing was carried out with the chrome devtools, with the next built-in devices.
- MotoG4
- Galaxy S5
- Pixel 2
- Pixel 2XL
- iPhone 6/7/8
- iPad
- iPad Pro
- Galaxy Fold
- Full HD laptop Screen
- Full HD 27" display

## Deployment

### Future Features
- Bootstrap 4 offers a bunch of components to help to have an app/site up and running, but some of them cuase a lot of problems on small screens, due to this reason, the project will be rebuilt with pure **CSS** to have full control of each component and how it will behaive on each screen size.

- For the register will be added a function to find an existing user to let know the user through **flash** in flask.

- For the Login will be added a funciton to let know the user when either username or password are incorrect.

- In new post will be added a function to detect a repeated post either through the post title or subtitle.

- When creating a new user will be added an avatar selector, and will be added an option to change/select the avatar in the users site.


## Special Thanks
- My mentor Guido Cecilio
- Code Institute Tutors Team
- [Pretty Printed](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)
- [Stackoverflow](https://stackoverflow.com/)