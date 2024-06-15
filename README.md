# Data Pusher

## About

This project is a FastAPI application designed to handle accounts and destinations. It provides functionality to manage accounts, associate destinations with accounts, and forward data to multiple destinations based on account configurations.

## Features

- **Account Management**:
  - Create, read, update, and delete accounts.
  - Generate unique app secret tokens for each account.
  - Associate optional website URLs with accounts.

- **Destination Management**:
  - Create, read, update, and delete destinations associated with accounts.
  - Specify URL, HTTP method (GET, POST, PUT, etc.), and headers for each destination.

- **Data Forwarding**:
  - Receive JSON data with an app secret token via a POST endpoint.
  - Identify the account associated with the token.
  - Forward received data to all configured destinations for that account based on HTTP methods.

### Screenshots
![alt text](<Screenshot from 2024-06-15 14-11-36.png>)

## Endpoints

### Accounts

- **Create Account**
  - **POST** `/accounts/`
  - Body: JSON data with `email`, `account_name`, and optional `website`.
  - Creates a new account with a unique app secret token.

- **Get Account**
  - **GET** `/accounts/{account_id}/`
  - Retrieves account details by `account_id`.

- **Update Account**
  - **PUT** `/accounts/{account_id}/`
  - Body: JSON data with fields to update (`account_name` and `website`).
  - Updates account details.

- **Delete Account**
  - **DELETE** `/accounts/{account_id}/`
  - Deletes an account by `account_id`.

- **Get All Accounts**
  - **GET** `/accounts/`
  - Retrieves a list of all accounts.

### Destinations

- **Create Destination**
  - **POST** `/accounts/{account_id}/destinations/`
  - Body: JSON data with `url`, `http_method` (GET, POST, PUT, etc.), and `headers`.
  - Creates a new destination associated with an account.

- **Get Destination**
  - **GET** `/destinations/{destination_id}/`
  - Retrieves destination details by `destination_id`.

- **Update Destination**
  - **PUT** `/destinations/{destination_id}/`
  - Body: JSON data with fields to update (`url`, `http_method`, and `headers`).
  - Updates destination details.

- **Delete Destination**
  - **DELETE** `/destinations/{destination_id}/`
  - Deletes a destination by `destination_id`.

- **Get All Destinations**
  - **GET** `/accounts/{account_id}/destinations/`
  - Retrieves all destinations associated with an account.

## Setting Up the Project

To run the project locally, follow these steps:

- **Clone the Repository:**
   ```bash
   git clone git@github.com:imrohitoberoi/datapusher.git
   cd datapusher

- **Pipenv Installation**:
  - Use `pipenv install` to install all project dependencies, including those specified in the Pipfile.

- **Environment Variables**:
  - Create `.env` file using `.env.template` file and fill the appropriate variables.

- **MySQL setup**:
  - Run Mysql server in your local, create a new database and user with appropriate permissions.
  - Add the details in `.env` file as mentioned.

- **VirtualEnv & Installing dependencies**:
  - Make sure you have `pipenv` installed in your device
  - Activate the Pipenv shell (`pipenv shell`) to ensure dependencies are accessed within the virtual environment.
  - Install all the dependencies mentioned in pipfile using command `pipenv install`

- **Migrations**:
  - Run below commands to apply database migrations defined by Tortoise ORM based on your model definitions.
  ```bash
  aerich init -t config.TORTOISE_ORM
  aerich init-db

- **Starting FastAPI Server**:
  - Use `uvicorn main:app --reload` to start the FastAPI server.

- **Accessing Documentation**:
  - Use url `http://localhost:8000/docs` to access the interactive Swagger UI documentation for API endpoints and test the working.


### Developed by Rohit Oberoi
