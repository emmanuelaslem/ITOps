from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)


@app.route("/")
def home():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            tickets.ticket_id,
            tickets.title,
            tickets.description,
            tickets.priority,
            tickets.status,
            employee.first_name AS employee_first_name,
            employee.last_name AS employee_last_name,
            technician.first_name AS technician_first_name,
            technician.last_name AS technician_last_name,
            devices.device_name,
            devices.operating_system
        FROM tickets
        JOIN users AS employee
            ON tickets.created_by = employee.user_id
        JOIN users AS technician
            ON tickets.assigned_to = technician.user_id
        JOIN devices
            ON tickets.device_id = devices.device_id
    """

    cursor.execute(query)
    all_tickets = cursor.fetchall()

    total_tickets = len(all_tickets)

    open_tickets = 0
    in_progress_tickets = 0
    resolved_tickets = 0

    for ticket in all_tickets:
        if ticket["status"] == "Open":
            open_tickets = open_tickets + 1

        if ticket["status"] == "In Progress":
            in_progress_tickets = in_progress_tickets + 1

        if ticket["status"] == "Resolved":
            resolved_tickets = resolved_tickets + 1

    cursor.execute("SELECT COUNT(*) AS total_devices FROM devices")
    device_result = cursor.fetchone()
    total_devices = device_result["total_devices"]

    search = request.args.get("search", "")
    status_filter = request.args.get("status", "All")
    priority_filter = request.args.get("priority", "All")

    tickets = []

    for ticket in all_tickets:
        matches_search = True
        matches_status = True
        matches_priority = True

        if search != "":
            search_text = search.lower()

            title = ticket["title"].lower()
            description = ticket["description"].lower()

            if search_text not in title and search_text not in description:
                matches_search = False

        if status_filter != "All":
            if ticket["status"] != status_filter:
                matches_status = False

        if priority_filter != "All":
            if ticket["priority"] != priority_filter:
                matches_priority = False

        if matches_search and matches_status and matches_priority:
            tickets.append(ticket)

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        tickets=tickets,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        resolved_tickets=resolved_tickets,
        total_devices=total_devices,
        search=search,
        status_filter=status_filter,
        priority_filter=priority_filter
    )


@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        employee = request.form["employee"]
        device = request.form["device"]
        priority = request.form["priority"]
        technician = request.form["technician"]

        query = """
            INSERT INTO tickets
            (title, description, priority, status,
             created_by, assigned_to, device_id)
            VALUES (%s, %s, %s, 'Open', %s, %s, %s)
        """

        values = (
            title,
            description,
            priority,
            employee,
            technician,
            device
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    cursor.execute("""
        SELECT user_id, first_name, last_name
        FROM users
        WHERE role = 'Employee'
    """)
    employees = cursor.fetchall()

    cursor.execute("""
        SELECT user_id, first_name, last_name
        FROM users
        WHERE role = 'Technician'
    """)
    technicians = cursor.fetchall()

    cursor.execute("""
        SELECT device_id, device_name, operating_system
        FROM devices
    """)
    devices = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "create_ticket.html",
        employees=employees,
        technicians=technicians,
        devices=devices
    )


@app.route("/update-ticket/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
    new_status = request.form["status"]

    if new_status in ["Open", "In Progress", "Resolved"]:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """
            UPDATE tickets
            SET status = %s
            WHERE ticket_id = %s
        """

        cursor.execute(query, (new_status, ticket_id))
        connection.commit()

        cursor.close()
        connection.close()

    return redirect(url_for("home"))


@app.route("/devices")
def devices():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            devices.device_id,
            devices.device_name,
            devices.device_type,
            devices.operating_system,
            devices.ip_address,
            devices.status,
            users.first_name,
            users.last_name
        FROM devices
        JOIN users
            ON devices.assigned_user_id = users.user_id
    """

    cursor.execute(query)
    device_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "devices.html",
        devices=device_list
    )


@app.route("/create-device", methods=["GET", "POST"])
def create_device():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        device_name = request.form["device_name"]
        device_type = request.form["device_type"]
        operating_system = request.form["operating_system"]
        ip_address = request.form["ip_address"]
        status = request.form["status"]
        assigned_user = request.form["assigned_user"]

        query = """
            INSERT INTO devices
            (device_name, device_type, operating_system,
             ip_address, status, assigned_user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            device_name,
            device_type,
            operating_system,
            ip_address,
            status,
            assigned_user
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("devices"))

    cursor.execute("""
        SELECT user_id, first_name, last_name, role
        FROM users
    """)

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "create_device.html",
        users=users
    )


if __name__ == "__main__":
    app.run(debug=True)