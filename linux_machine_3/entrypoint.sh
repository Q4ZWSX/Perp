#!/bin/bash

# Check if TEAMLOGIN_PASSWORD is set
if [ -z "$TEAMLOGIN_PASSWORD" ]; then
    echo "Error: TEAMLOGIN_PASSWORD environment variable not set"
    exit 1
fi

# Create teamlogin user if it doesn't exist
id teamlogin >/dev/null 2>&1 || useradd -m -s /bin/bash teamlogin

# Set the password for teamlogin
echo "teamlogin:$TEAMLOGIN_PASSWORD" | chpasswd

# Grant sudo privileges without password prompt
echo "teamlogin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/teamlogin
chmod 0440 /etc/sudoers.d/teamlogin

# Ensure SSH directory exists for teamlogin
mkdir -p /home/teamlogin/.ssh
chown teamlogin:teamlogin /home/teamlogin/.ssh
chmod 700 /home/teamlogin/.ssh

# Start SSH server in the background
echo "Starting SSH server on port 22..."
/usr/sbin/sshd &

# Start Flask application
echo "Starting Flask application on port 5000..."
exec python3 /app/app.py
