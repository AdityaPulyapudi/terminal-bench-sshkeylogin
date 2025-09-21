import os
import paramiko
import pytest
import stat

SERVER = "server"
USER = "devops"
PASSWORD = "devops"

def ssh_connect_with_key():
    key = paramiko.RSAKey.from_private_key_file(f"/home/{USER}/.ssh/id_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER, username=USER, pkey=key)
    return client

def test_keypair_exists():
    assert os.path.exists(f"/home/{USER}/.ssh/id_rsa")
    assert os.path.exists(f"/home/{USER}/.ssh/id_rsa.pub")

def test_authorized_keys_exists():
    assert os.path.exists(f"/home/{USER}/.ssh/authorized_keys")

def test_permissions():
    st_dir = os.stat(f"/home/{USER}/.ssh")
    st_file = os.stat(f"/home/{USER}/.ssh/authorized_keys")
    assert stat.S_IMODE(st_dir.st_mode) == 0o700, ".ssh dir must be 700"
    assert stat.S_IMODE(st_file.st_mode) == 0o600, "authorized_keys must be 600"

def test_sshd_config_pubkey_enabled():
    with open("/etc/ssh/sshd_config") as f:
        data = f.read()
    assert "PubkeyAuthentication yes" in data

def test_sshd_config_password_disabled():
    with open("/etc/ssh/sshd_config") as f:
        data = f.read()
    assert "PasswordAuthentication no" in data

def test_login_without_password():
    client = ssh_connect_with_key()
    stdin, stdout, stderr = client.exec_command("whoami")
    assert stdout.read().decode().strip() == USER
    client.close()
