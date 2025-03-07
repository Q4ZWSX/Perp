FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install required packages (including Apache)
RUN apt-get update -y && \
    apt-get install -y git apache2

# 2. Clone the existing FTP-related repository
WORKDIR /root/
RUN git clone https://github.com/Anon-Exploiter/vulnerable-packages && \
    cd vulnerable-packages && \
    cd backdoored-vsftpd-2.3.4 && \
    mv * /root/ && \
    cd /root && \
    rm -rfv vulnerable-packages

# 3. Remove git and clean
RUN apt-get purge -y git && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    apt-get -y clean

# 4. Create necessary FTP directories and user
RUN mkdir -p /usr/share/empty/ && \
    mkdir -p /var/ftp/ && \
    useradd -d /var/ftp ftp && \
    chown root.root /var/ftp && \
    chmod og-w /var/ftp

# 5. Move vsftpd binaries/config in place
RUN mv vsftpd /usr/local/sbin/vsftpd && \
    mv vsftpd.conf /etc/

# 6. Create some basic web pages
RUN echo '<html><head><title>Index</title></head><body><h1>Index of Pages</h1><ul>' \
         '<li><a href="page1.html">Page 1</a></li>' \
         '<li><a href="page2.html">Page 2</a></li>' \
         '<li><a href="page3.html">Page 3</a></li>' \
         '</ul></body></html>' \
    > /var/www/html/index.html

RUN echo '<html><head><title>Page 1</title></head><body><h2>Page 1</h2></body></html>' \
    > /var/www/html/page1.html

RUN echo '<html><head><title>Page 2</title></head><body><h2>Page 2</h2></body></html>' \
    > /var/www/html/page2.html

RUN echo '<html><head><title>Page 3</title></head><body><h2>Page 3</h2></body></html>' \
    > /var/www/html/page3.html

# 7. Create a run script that starts vsftpd in the background,
#    then runs Apache in the foreground so the container stays alive.
RUN echo '#!/bin/bash\n' \
         'echo "Starting vsftpd (FTP) on port 21 and 6200..." \n' \
         '/usr/local/sbin/vsftpd &\n' \
         'echo "Starting Apache HTTP Server on port 80..." \n' \
         'exec apache2ctl -D FOREGROUND\n' \
    > /root/run.sh && chmod +x /root/run.sh

# 8. Expose the ports (21 and 6200 for FTP; 80 for Apache)
EXPOSE 21 6200 80

# 9. Set default command to run the script
CMD ["/bin/bash", "/root/run.sh"]
