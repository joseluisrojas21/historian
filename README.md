# Historian Server for ICS

This project is a historian server for ICS (Industrial Control Systems), built to graph records stored in a SQLite3 database. It uses a combination of Node.js, Svelte, and Nginx to serve a web interface that visualizes historical data. The server is initialized and managed via a systemd service, which runs a shell script (`historian.sh`) to start the necessary services at boot.

## Features

- **SQLite3 Database Integration**: Reads historical records from a SQLite3 database.
- **Real-Time Visualization**: Displays the data using dynamic graphs on the web interface.
- **Web Interface**: Built with Svelte, served by Node.js.
- **Systemd Service**: Automatically starts the web server at boot time using a systemd service (`historian.service`).
- **Nginx Reverse Proxy**: Serves the application with Nginx, handling both static and dynamic content.

## Requirements

- **Node.js**: Used to run the server and handle application logic.
- **npm**: Used for managing JavaScript dependencies and running development scripts.
- **Svelte**: Frontend framework used to create the web interface for displaying historical data.
- **SQLite3**: Database system for storing historical records.
- **Nginx**: Web server to serve the application and reverse proxy requests to the Node.js server.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/historian.git
cd historian
```
### 2. Install Dependencies
```bash
npm install
```

### 3. Setup Systemd Service
```bash
sudo nano /etc/systemd/system/historian.service
```
Add the following content:

```bash
[Unit]
Description=Historian Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/historian
ExecStart=/bin/bash /var/www/historian/historian.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Setup the Shell Script
Create a shell script (historian.sh) to run the necessary commands to start the application:
```bash
sudo nano /var/www/historian/historian.sh
```

Add the following content:
```bash
#!/bin/bash
cd /var/www/historian
/usr/bin/npm run dev &
/usr/bin/node /var/www/historian/server/server.js
```

Make the script executable:
```bash
sudo chmod +x /var/www/historian/historian.sh
```

### 5. Set Permissions
Set the correct permissions and ownership for the files:
```bash
sudo chmod -R 755 /var/www/historian
sudo chown -R www-data:www-data /var/www/historian
```

### 6. Reload Systemd and Enable the Service
Reload the systemd configuration and enable the historian service to start on boot:
```bash
sudo systemctl daemon-reload
sudo systemctl enable historian.service
sudo systemctl start historian.service
```

### 7. Configure Nginx
```bash
Create the Nginx configuration file to serve the application:
sudo nano /etc/nginx/sites-available/default
```

Add the following content:
```bash
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/historian;

    server_name 192.168.100.183 100.108.218.111;

    location /_app/ {
        root /.svelte-kit/output/server;
        try_files $uri $uri/ =404;
    }

    location /chunks/ {
        root /.svelte-kit/output/server;
    }

    location /stylesheets/ {
        root /.svelte-kit/output/server;
    }

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 8. Restart Nginx
Restart the Nginx service to apply the configuration:
```bash
sudo systemctl restart nginx
```

# Usage

### Starting the Server
The server should now be running as a service. You can start, stop, or check the status of the historian service using systemctl:
```bash
sudo systemctl start historian.service
sudo systemctl stop historian.service
sudo systemctl status historian.service
```

To view logs and debug issues:
```bash
sudo journalctl -u historian.service -n 50
```

### Accessing the Web Interface
The web application will be available at the IP addresses specified in the Nginx configuration (e.g., http://100.108.218.111).