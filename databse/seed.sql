USE ITOps;

INSERT INTO users (first_name, last_name, email, role)
VALUES
('Marcus', 'Johnson', 'marcus.johnson@demo.com', 'Employee'),
('Sarah', 'Williams', 'sarah.williams@demo.com', 'Employee'),
('David', 'Chen', 'david.chen@demo.com', 'Technician'),
('Maya', 'Thompson', 'maya.thompson@demo.com', 'Technician');


INSERT INTO devices
(device_name, device_type, operating_system, ip_address, status, assigned_user_id)
VALUES
('LT-001', 'Laptop', 'Windows 11', '192.168.1.21', 'Active', 1),
('LT-002', 'Laptop', 'macOS', '192.168.1.22', 'Active', 2),
('DT-001', 'Desktop', 'Windows 11', '192.168.1.23', 'Active', 3);

INSERT INTO tickets
(title, description, priority, status, created_by, assigned_to, device_id)
VALUES
('Wi-Fi connection issue',
 'Laptop keeps disconnecting from the company Wi-Fi.',
 'High',
 'Open',
 1,
 3,
 1),

('Computer running slowly',
 'Employee reports that the laptop has been running slowly.',
 'Medium',
 'In Progress',
 2,
 4,
 2);