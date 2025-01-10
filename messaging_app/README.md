## Tasks

### 0\. project set up

mandatory


**Objective:** create a new django project and install django rest framework

**Instructions:**

- Initialize a new django project `django-admin startproject messaging_app`
    
- Install django REST Framework and set it up in the `settings.py`
    
- Create a new app for the messaging functionality. (`python manage.py startapp chats`)
    

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `messaging_app`
- File: `messaging_app/*`





### 1\. Define data Models

mandatory

**Objective:** Design the models for users, messages, and conversations.

**Instructions:**

- Using the tables definition described above,
    
    - Create the `user` Model an extension of the Abstract user for values not defined in the built-in Django `User` model
    - Create the `conversation` model that tracks which users are involved in a conversation
    - Create the `message` model containing the sender, conversation as defined in the shared schema attached to this project

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `messaging_app`
- File: `messaging_app/chats/models.py`


### 2\. create serializers to define the many to many relationships

mandatory

Score: 0.0% (Checks completed: 0.0%)

**Objective**: build serializers for the models

**Instructions:**

- Create Serializers for `Users, conversation` and `message`
    
- Ensure nested relationships are handled properly, like including messages within a conversation
    

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `messaging_app`
- File: `messaging_app/chats/serializers.py`





### 3\. Build api endpoints with views

mandatory

**Objective:** implement API endpoints for conversations and messages

**Instructions:**

- Using `viewsets from rest-framework` Create viewsets for listing conversations (`ConversationViewSet`) and messages (`MessageViewSet`)
    
- Implement the endpoints to create a new conversation and send messages to an existing one
    

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `messaging_app`
- File: `messaging_app/chats/views.py`




### 5\. Run the application to fix errors

mandatory

Score: 0.0% (Checks completed: 0.0%)

**Objective:** run and test the applications

**Instructions:**

- Run python manage.py makemigrations, python manage.py migrate, python manage.py runserver to test and run the application
    
- Fix any error or bugs produced
    

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `messaging_app`
