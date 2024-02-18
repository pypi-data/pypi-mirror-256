import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "start","lewagon-data-eng-vm-sergiofrfo-google"])

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "stop","lewagon-data-eng-vm-sergiofrfo-google"])

@click.command()
def connect():
    """Connect to your vm"""
    subprocess.run(["code", "--folder-uri",
        "vscode-remote://ssh-remote+sergiofrfo@34.77.239.138/home/sergiofrfo/code/sergiofrfo-google"])
