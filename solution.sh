#!/bin/bash
set -e

# On client
sudo -u devops ssh-keygen -t rsa -N "" -f /home/devops/.ssh/id_rsa

# Copy public key to server
sshpass -p "devops" ssh-copy-id -o StrictHostKeyChecking=no devops@server

# Fix permissions
ssh server "chmod 700 /home/devops/.ssh && chmod 600 /home/devops/.ssh/authorized_keys"

# Update sshd_config
ssh server "sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && sudo systemctl restart ssh"
