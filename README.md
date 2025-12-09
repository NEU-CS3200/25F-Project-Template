# Fresh Routes Web Application

Welcome! This repository contains all files needed to launch our Fresh Routes App on your computer!

This project was developed by five Northeastern University Students while on the Fall Semester 2025 for Introduction to Dataframes.

More about the developers can be viewed on the About page on our app.

# What is Fresh Routes

Fresh Routes is a comprehensive web application that connects four distinct user types: Customer, Farmer, Driver, and Admin.

While there exist meal kit delivery companies that provide pre-thought out meals for customers, there's no other platform that works with local farmers to make sure the ingredients are the highest quality. Fresh Routes connects with all personas to ensure a unique and personalized experience. 
Customers get to customize their meal planning experience and delivery
Farmers are able to input their produce and see future predictions to plan accordingly
Drivers control their schedule and get real life traffic updates based on their route 
Admins analyze feedback through chats and engagement to create new recipes and optimize overall experience 

From a busy customer to a farmer, to a driver and even an admin, Fresh Routes transforms a problem into a customizable solution. 

## Theory to Functionality
In order to implement our idea into a functioning web-app, we implemented 4 aspects to our app. 

### **StreamLit And FrontEnd**
Our group used Streamlit's Python library to create interactive dashboards for each user. The main focus of using Streamlit was to create a user friendly interface, with the developer-side motivation being the ability to build functional frontends without extensive web development knowledge.
All four personas could interact with the web application through dynamic charts, filters, and predictive analytics displays that streamlit supported.  

### **Flask API**
Utilizing the Flask Library in Python, we implemented a RESTful Flask API to manage mockdata operations through HTTP methods. Implemented GET endpoints to display existing data to the user in the form of a visualization or text, POST endpoints for creating new records, PUT endpoints for updating existing data, and DELETE endpoints for removing entries from the MySQL database. The API served as the backend interface, processing incoming HTTP requests, executing corresponding SQL operations, and returning appropriate JSON responses to maintain seamless frontend-database communication

## How to Access

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- VSCode with the Python Plugin
- A distribution of Python running on your laptop. The distribution supported by the course is Anaconda or Miniconda.

## Structure of Our Repo

- The repo is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets
  - `./ml-src` - folder for storing ML models
- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. This file is used to run the app and API in Docker containers.

Massimo Prag, MYSQL_ROOT_PASSWORD = yourpassword123
Emma Kulla, MYSQL_ROOT_PASSWORD = Em1205ma!
Maria Samos Rivas, MYSQL_ROOT_PASSWORD = good_1290
Katherine Datlow, MYSQL_ROOT_PASSWORD = Wessy612!
Brianna Fountain, MYSQL_ROOT_PASSWORD = 12334

# Final Video
https://youtu.be/FwrAARnJktk
