import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "start",
                "lewagon2-data-eng-vm-kiady-andria"])

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "stop",
                "lewagon2-data-eng-vm-kiady-andria"])

@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/kiady-andria/folder """
    subprocess.run(["code", "--folder-uri",
        "vscode-remote://ssh-remote+kiady.andrianantoandro@34.76.204.236/home/kiady-andria/"])
