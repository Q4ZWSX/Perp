# Setting Up an OpenVPN Server on AWS EC2 with Docker Compose

This guide provides detailed instructions for launching an AWS EC2 instance, installing necessary tools, transferring a zip file containing a Docker Compose setup for an OpenVPN server, running the server, configuring it with the EC2 instance's public IP, and distributing OpenVPN credentials to teams.

## Prerequisites
- AWS account with permissions to create EC2 instances
- SSH client (e.g., OpenSSH on Linux/Mac or PuTTY on Windows)
- Local machine with `magic-wormhole` installed (`pip install magic-wormhole`)
- A clone of this repository
- Team names and passwords (example placeholders):
  - Team1: password1
  - Team2: password2
  - Team3: password3
  - Team4: password4

## Step 1: Launch a Large EC2 Instance
1. Log in to the AWS Management Console and navigate to the EC2 Dashboard.
2. Click **Launch Instance** and configure:
   - **Name**: `OpenVPN-Server`
   - **AMI**: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
   - **Instance Type**: `t2.large` (or another large instance type)
   - **Key Pair**: Create or select an existing key pair
   - **Storage**: 30 GiB gp3 (adjust as needed)
3. Review and click **Launch Instance**.
4. Note the instance’s public IP address from the EC2 Instances page.

## Step 2: SSH into the EC2 Instance
1. Ensure your key pair file has the correct permissions:
```bash
chmod 400 key.pem
```
2. Connect to the instance, replacing `<EC2_PUBLIC_IP>` with the instance’s public IP:
```bash
ssh -i openvpn-key.pem ubuntu@<EC2_PUBLIC_IP>
```
Example:
```bash
ssh -i openvpn-key.pem ubuntu@203.0.113.10
```

## Step 3: Install unzip
Update the package list and install `unzip`:
```bash
sudo apt update
sudo apt install -y unzip
```

## Step 4: Install magic-wormhole
Install `magic-wormhole` to receive the zip file:
```bash
sudo apt install magic-wormhole
```

## Step 5: Install Docker Compose
Install Docker and Docker Compose using the official Ubuntu repository method.
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
1. Update the package index and install prerequisites:
```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

2. Add the Docker repository to APT sources:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

## Step 6: Transfer the Zip File via magic-wormhole
1. On your local machine, send the zip file (e.g., `perp.zip`):
```bash
wormhole send perp.zip
```
Copy the generated wormhole code (e.g., `7-crossover-clockwork`).

2. On the EC2 instance, receive the zip file using the wormhole code:
```bash
wormhole receive
```
Enter the wormhole code when prompted, then confirm the file transfer (e.g., `y` to save as `perp.zip`).

## Step 7: Unzip the File
Unzip the transferred file:
```bash
unzip perp.zip
```
This extracts the `docker-compose.yml` and related files into the current directory.

## Step 8: Run Docker Compose
Build and start the OpenVPN service:
```bash
docker compose up
```
Wait for the command to complete (this may take a few minutes as it builds and starts the containers).

## Step 9: Access the OpenVPN Admin Panel
1. Open a web browser and navigate to:
```
http://<EC2_PUBLIC_IP>:8000
```
Example:
```
http://203.0.113.10:8000
```

## Step 10: Update Configuration with EC2 Public IP
1. Edit the OpenVPN configuration to include the EC2 instance’s public IP. Assume the `docker-compose.yml` or a related config file (e.g., `client.conf`) needs the public IP.
2. Open the file (adjust the path/filename based on your setup):
```bash
nano client.conf
```
3. Update the server address to the EC2 public IP, e.g.:
```
remote 203.0.113.10 1194 udp
```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

5. Connect to the openvpn server:
```
sudo openvpn client.conf
```

## Step 12: Add Teams and Passwords
In the OpenVPN admin panel at `http://172.30.0.16:5000/admin`:
1. Navigate to the user management section.
2. Add each team with their corresponding password:
   - Team1: password1
   - Team2: password2
3. Save the changes.

## Step 13: Distribute OVPN Files and Passwords
1. Securely transfer a `.ovpn` file to each team.
2. Communicate the corresponding password to each team securely
   - Team1: `Team1.ovpn`, Password: `password1`
   - Team2: `Team2.ovpn`, Password: `password2`

For issues, refer to:
- Docker documentation: https://docs.docker.com
- OpenVPN documentation: https://openvpn.net
- AWS EC2 User Guide: https://docs.aws.amazon.com/ec2
