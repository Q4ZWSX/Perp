# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && apt-get install -y \
    openvpn \
    easy-rsa \
    openssh-server \
    python3 \
    iptables \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /etc/openvpn/server /etc/openvpn/client /etc/openvpn/easy-rsa /var/www/html

# Copy easy-rsa to openvpn directory and set up CA
WORKDIR /etc/openvpn/easy-rsa
RUN cp -r /usr/share/easy-rsa/* /etc/openvpn/easy-rsa/
COPY ./vars ./vars

# Generate certificates and keys
RUN ./easyrsa init-pki && \
    ./easyrsa --batch build-ca nopass && \
    ./easyrsa gen-dh && \
    ./easyrsa build-server-full server nopass && \
    ./easyrsa build-client-full client nopass && \
    openvpn --genkey --secret ta.key

# Copy certificates and keys to appropriate locations
RUN cp pki/ca.crt pki/private/ca.key pki/dh.pem pki/issued/server.crt pki/private/server.key ta.key /etc/openvpn/server/ && \
    cp pki/ca.crt pki/issued/client.crt pki/private/client.key ta.key /etc/openvpn/client/

# Create OpenVPN server configuration
RUN echo "port 1194" > /etc/openvpn/server.conf && \
    echo "proto udp" >> /etc/openvpn/server.conf && \
    echo "dev tun" >> /etc/openvpn/server.conf && \
    echo "ca /etc/openvpn/server/ca.crt" >> /etc/openvpn/server.conf && \
    echo "cert /etc/openvpn/server/server.crt" >> /etc/openvpn/server.conf && \
    echo "key /etc/openvpn/server/server.key" >> /etc/openvpn/server.conf && \
    echo "dh /etc/openvpn/server/dh.pem" >> /etc/openvpn/server.conf && \
    echo "tls-auth /etc/openvpn/server/ta.key 0" >> /etc/openvpn/server.conf && \
    echo "server 10.8.0.0 255.255.255.0" >> /etc/openvpn/server.conf && \
    echo "push \"route 172.30.0.0 255.255.255.0\"" >> /etc/openvpn/server.conf && \
    echo "push \"route 172.30.1.0 255.255.255.0\"" >> /etc/openvpn/server.conf && \
    echo "push \"route 172.30.2.0 255.255.255.0\"" >> /etc/openvpn/server.conf && \
    echo "push \"route 172.30.3.0 255.255.255.0\"" >> /etc/openvpn/server.conf && \
    echo "push \"route 172.30.4.0 255.255.255.0\"" >> /etc/openvpn/server.conf && \
    echo "topology subnet" >> /etc/openvpn/server.conf && \
    echo "keepalive 10 120" >> /etc/openvpn/server.conf && \
    echo "data-ciphers AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305" >> /etc/openvpn/server.conf && \
    echo "persist-key" >> /etc/openvpn/server.conf && \
    echo "persist-tun" >> /etc/openvpn/server.conf && \
    echo "verb 3" >> /etc/openvpn/server.conf && \
    echo "duplicate-cn" >> /etc/openvpn/server.conf && \
    echo "max-clients 200" >> /etc/openvpn/server.conf

# Create single OpenVPN client configuration
RUN echo "client" > /var/www/html/client.ovpn && \
    echo "dev tun" >> /var/www/html/client.ovpn && \
    echo "proto udp" >> /var/www/html/client.ovpn && \
    echo "remote <YOUR_PUBLIC_IP> 1194" >> /var/www/html/client.ovpn && \
    echo "resolv-retry infinite" >> /var/www/html/client.ovpn && \
    echo "nobind" >> /var/www/html/client.ovpn && \
    echo "persist-key" >> /var/www/html/client.ovpn && \
    echo "persist-tun" >> /var/www/html/client.ovpn && \
    echo "remote-cert-tls server" >> /var/www/html/client.ovpn && \
    echo "data-ciphers AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305" >> /var/www/html/client.ovpn && \
    echo "verb 3" >> /var/www/html/client.ovpn && \
    echo "route 172.30.0.0 255.255.255.0" >> /var/www/html/client.ovpn && \
    echo "route 172.30.1.0 255.255.255.0" >> /var/www/html/client.ovpn && \
    echo "route 172.30.2.0 255.255.255.0" >> /var/www/html/client.ovpn && \
    echo "route 172.30.3.0 255.255.255.0" >> /var/www/html/client.ovpn && \
    echo "route 172.30.4.0 255.255.255.0" >> /var/www/html/client.ovpn && \
    echo "<ca>" >> /var/www/html/client.ovpn && \
    cat /etc/openvpn/client/ca.crt >> /var/www/html/client.ovpn && \
    echo "</ca>" >> /var/www/html/client.ovpn && \
    echo "<cert>" >> /var/www/html/client.ovpn && \
    cat /etc/openvpn/client/client.crt >> /var/www/html/client.ovpn && \
    echo "</cert>" >> /var/www/html/client.ovpn && \
    echo "<key>" >> /var/www/html/client.ovpn && \
    cat /etc/openvpn/client/client.key >> /var/www/html/client.ovpn && \
    echo "</key>" >> /var/www/html/client.ovpn && \
    echo "<tls-auth>" >> /var/www/html/client.ovpn && \
    cat /etc/openvpn/client/ta.key >> /var/www/html/client.ovpn && \
    echo "</tls-auth>" >> /var/www/html/client.ovpn && \
    echo "key-direction 1" >> /var/www/html/client.ovpn

# Configure SSH
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Set up iptables for NAT and routing with logging
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'echo "Starting entrypoint script..."' >> /entrypoint.sh && \
    echo 'iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -d 172.30.0.0/16 -j MASQUERADE' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i tun0 -o eth0 -s 10.8.0.0/24 -d 172.30.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i eth0 -o tun0 -s 172.30.0.0/24 -d 10.8.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i tun0 -o eth1 -s 10.8.0.0/24 -d 172.30.1.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i eth1 -o tun0 -s 172.30.1.0/24 -d 10.8.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i tun0 -o eth2 -s 10.8.0.0/24 -d 172.30.2.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i eth2 -o tun0 -s 172.30.2.0/24 -d 10.8.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i tun0 -o eth3 -s 10.8.0.0/24 -d 172.30.3.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i eth3 -o tun0 -s 172.30.3.0/24 -d 10.8.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i tun0 -o eth4 -s 10.8.0.0/24 -d 172.30.4.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'iptables -A FORWARD -i eth4 -o tun0 -s 172.30.4.0/24 -d 10.8.0.0/24 -j ACCEPT' >> /entrypoint.sh && \
    echo 'echo "iptables rules applied"' >> /entrypoint.sh && \
    echo '/usr/sbin/sshd -D &' >> /entrypoint.sh && \
    echo 'openvpn --config /etc/openvpn/server.conf --verb 4 &' >> /entrypoint.sh && \
    echo 'python3 -m http.server 80 --directory /var/www/html &' >> /entrypoint.sh && \
    echo 'wait' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set permissions
RUN chmod 600 /etc/openvpn/server/* /etc/openvpn/client/*

# Expose ports (though docker-compose will handle the mapping)
EXPOSE 22 1194/udp 80

# Use entrypoint instead of command from docker-compose
ENTRYPOINT ["/entrypoint.sh"]
