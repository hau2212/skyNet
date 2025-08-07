import paramiko
import re
import time

class SSHClient:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        self.shell = self.client.invoke_shell()

    def send_command(self, command):
        if self.shell:
            self.shell.send(command + '\n')
            time.sleep(0.5)
            output = ''
            while self.shell.recv_ready():
                recv = self.shell.recv(4096).decode('utf-8', errors='ignore')
                output += recv
            cleaned = self.clean_output(output)
            return self.remove_command_echo(cleaned, command)
        return 'Shell is not ready.'

    def clean_output(self, text):
        ansi_escape = re.compile(r'''
            \x1B
            (?:[@-Z\\-_]|
            \[[0-?]*[ -/]*[@-~])
        ''', re.VERBOSE)
        return ansi_escape.sub('', text)

    def remove_command_echo(self, output, command):
        lines = output.splitlines()
        filtered = [line for line in lines if command not in line]
        return "\n".join(filtered)

    def close(self):
        if self.client:
            self.client.close()
