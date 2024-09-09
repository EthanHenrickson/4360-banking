# CS Banking App

## Introduction

This is a simple Python banking app that runs in the command line.

To get started, make sure you have the TinyDB installed. You can install it using pip with the command below. The backend uses a small local database to store accounts and info.

```
> pip install tinydb
```

Once tinyDB is installed you can start the app with the following command:

```
> python index.py
```

From there, you can just follow the prompts to get started using the bank. Otherwise you can continue reading the docs below.

For Justin - You can login using any account in the database to test it. I also have one here for you to use
username - ethanh
password - password

## Documentation

Below is documentation on the different functions and commands of the app. To enter a command, just enter the command in the terminal and hit enter.

### Creating and Logging In

Once the bank app is started you must either log in or Create a new account. This can be done by either of the following respective commands

`create account` - This allows you to create a new user account. After entering the command follow the prompts on the screen.

`login` - This will allow you to login to your bank account. After entering the command follow the prompts on the screen.

### Money Commands

`deposit` - This allows you too deposit money into your account. After entering the command follow the prompts on the screen.

`withdraw` - This allows you to withdraw money from your account. After entering the command follow the prompts on the screen.

`transfer` - This allows you too transfer money from your account to another users account given their username. After entering the command follow the prompts on the screen.

`get balance` - This will print out your current balance.

### Account Commands

`lock account` - This will lock your account. A locked account cannot withdraw, deposit, or withdraw money. After entering the command follow the prompts on the screen.

`unlock account` - This will unlock your account. After entering the command follow the prompts on the screen.

`log out` - This will log you out of your account.

### Misc Commands

`exit` - This will close the bank account
`help` - This returns a list of commands and descriptions
