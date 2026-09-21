# ITOps - IT Support & Asset Management System

ITOps is a web-based IT support and asset management application built to simulate a small organization's help desk environment.

The application allows IT staff to manage support tickets, track company devices, assign technicians, and monitor ticket status from a central dashboard.

## Features

- Create IT support tickets
- Assign tickets to technicians
- Track ticket priority and status
- Update tickets as Open, In Progress, or Resolved
- Search support tickets
- Filter tickets by status and priority
- View dashboard statistics
- Track company laptops and desktops
- Assign devices to users
- Add new devices to the inventory
- Store application data in a MySQL relational database

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- Jinja
- MySQL Connector/Python

## Database Structure

The system uses three main tables:

### Users
Stores employees and IT technicians.

### Devices
Stores company devices including:

- Device name
- Device type
- Operating system
- IP address
- Device status
- Assigned user

### Tickets
Stores IT support requests including:

- Ticket title
- Description
- Priority
- Status
- Employee
- Assigned technician
- Associated device
- Creation date

The tables are connected using primary and foreign keys.

## Application Workflow

1. Employees and devices are stored in the MySQL database.
2. A support ticket can be created from the web application.
3. Flask receives the form data and inserts the ticket into MySQL.
4. Tickets are displayed on the dashboard using SQL joins.
5. Technicians can update ticket statuses.
6. Dashboard statistics update automatically.

## Project Structure

```text
ITOps/
├── database/
│   ├── setup.sql
│   └── seed.sql
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── create_ticket.html
│   ├── devices.html
│   └── create_device.html
├── app.py
├── requirements.txt
├── README.md
└── .gitignore