<div align='center'>

    # Questioner
    <span> Where Questions Drive Agenda <span>
    [![Build Status](https://travis-ci.org/da-tinker/questioner.svg?branch=develop)](https://travis-ci.org/da-tinker/questioner)
    [![Coverage Status](https://coveralls.io/repos/github/da-tinker/questioner/badge.svg?branch=develop)](https://coveralls.io/github/da-tinker/questioner?branch=develop)
    [![Maintainability](https://api.codeclimate.com/v1/badges/2cada0d526a4ef023891/maintainability)](https://codeclimate.com/github/da-tinker/questioner/maintainability)
    [![Test Coverage](https://api.codeclimate.com/v1/badges/2cada0d526a4ef023891/test_coverage)](https://codeclimate.com/github/da-tinker/questioner/test_coverage)

</div>

# Project Overview
Questioner is a platform to crowd-source questions for a meetup i.e. attendees of a meetup get to post questions that they would like discussed during the meetup.

Attendees can cast votes on questions and this enables the meetup organizer(s) to prioritize questions to be discussed.

## Primary Features 
1. Admin can create meetups. 
2. Users can create an account and log in. 
3. Users can post questions to a specific meetup. 
4. Users can upvote or downvote a question. 
5. Questions are sorted based on the number of upvotes a question has, which helps the meetup organizer(s) to prioritize questions most users are interested in.
6. Users can post comments to a specific question. 

## Optional Features
1. Admin can add images to a meetup record. 
2. Admin can add tags to a meetup record. 
3. User can reset password. 

# Getting started
This guide addresses the REST API server component of Questioner

## Installation
1. Clone the repository
   
   ```bash
$ git clone https://github.com/da-tinker/questioner.git
   ```

2. Navigate to project folder
   
   ```bash
    $ cd questioner
   ```

3. Ensure you're on the develop branch
```bash
$ git checkout develop
```
4. Activate the virtual environment

   ```bash
$ source env/bin/activate
   ```

5. Install requirements

   ```bash
$ pip install -r requirements.txt
   ```

## Run the app
   ```bash
$ flask run
   ```
The api server is now running locally and can be reached on: `http://localhost:5000/`

## Testing
1. Source code unit tests
   Navigate to app directory
   ```bash
    $ cd app
   ```
   Execute pytest against the tests directory
   ```bash
   $ pytest tests/
   ```
2. API Endpoints functionality  
   You can use [Postman](https://www.getpostman.com/) to test the endpoints

## Endpoints
| Request Method       | EndPoint       | Functionality |
| ------------- | ------------- | ---------------
| POST  | `/api/v1/meetups`  | Create a new meetup record   |
| GET  | `/api/v1/meetups/<meetup_id>`  | Fetch a specific meetup record  |
| GET  | `/api/v1/meetups/upcoming/`   | Fetch all upcoming meetup records   |
| POST  | `/api/v1/meetups/<meetup_id>/rsvps`   | RSVP to meetup   |
|
| POST  | `/api/v1/questions` | Create a question for a specific meetup.   |
| PATCH | `/api/v1/questions/<question_id>/upvote` | Add vote count for question by one |
| PATCH | `/api/v1/questions/<question_id>/downvote` | Decrease vote count for question by one  |

## Acknowledgments
Andela Kenya:
- slack nbo-36
- nbo-36 Team 12 members

## Author
[Matthew Adote](https://github.com/da-tinker)