# SITTV Barcode System Specification

## Introduction
In order to establish a more consistent and traceable system for the management of SITTV equipment, a new system shall be put into place in order to ease the administration of operations.

The lack of a proper equipment management system has needlessly tasked members, and made operations difficult.

## Requirements
The system in question should be similar to library self check-out/in system.
Verified users will be able to login with their username/production, scan the items needed for the production, and log their usage.

### Database Requirements
* List of user names and cwid's
* List of productions
* Barcode, name (and possibly pictures)
* Ability to keep track of who has what privileges.
### Touch-screen UI Requirements
* Ability to login by name/cwid pair
* Ability to sign in by production 
* Autogeneration of forms
* Automatic return (regardless of user login)
### Backend UI
* Ability to check out who/which productions are in possession of what equipment.
* Usage statistics based on logs (what equipment is used by most, by whom, etc.)
### Notification Bot
* __Bookie Bot__ *the bot that comes after you if you don't return what you owe* 
* Slack bot for overdue item notifications
* Contacts necessary parties (user, producer, director of operations, etc.)

## Design Considerations
### Database
* Containerize the database (most likely using Docker)
### Web App
* Use a standard scripting language such as Python or NodeJS.
### Touch Screen
* Integration of a card-swipe system to expedite login on the touch screen.
* Item entry by barcode and calendar selector (for date-until).

## Repository Structure
Until the project matures, we will place all of the source code into the [sittv/barcodes](https://github.com/sittv/barcodes) repository.
The structure of the repository should look similar to:
```
.
├── bookiebot
├── db
├── touchscreen
└── webapp
```
With each subdirectory containing all of the code for the relevant sub-project.

## Prototype Specification
| Component        | Tool    |
|------------------|---------|
| Database         | MongoDB |
| Language         | Python  |
| Web Framework    | Flask   |
| Containerization | Docker  |

### Database Specification
#### User
| Field          | Type           |
|----------------|---------------:|
| Name           | string         |
| Username/email | string         |
| CWID           | int64          |
| Productions    | list of string |
#### Item
| Field    | Type     |
|----------|---------:|
| Name     | string   |
| Barcode  | int64    |
| Checkout | Checkout |
#### Checkout
| Field         | Type               |
|---------------|-------------------:|
| Who           | user name (string) |
| Production    | string             |
| Checkout Date | date               |
| Until When    | date               |
