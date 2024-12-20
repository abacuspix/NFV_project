# coding:utf-8

from fabric import Connection

# Define the host details
HOST = "your.host.ip.address"
REPO = "git://path/to/repo.git"
PROJECT_DIR = "~/project"

# Connect to the remote server
def get_connection():
    return Connection(HOST, forward_agent=True)

def create_project():
    """
    Clones the repository if it doesn't exist.
    """
    conn = get_connection()
    if not conn.run(f'test -d {PROJECT_DIR}', warn=True).ok:
        conn.run(f'git clone {REPO} {PROJECT_DIR}')
    else:
        print("Project directory already exists.")

def update_code():
    """
    Pulls the latest changes from the repository.
    """
    conn = get_connection()
    with conn.cd(PROJECT_DIR):
        conn.run('git pull')

def reload():
    """
    Triggers a reload of the project.
    """
    conn = get_connection()
    conn.run('touch --no-dereference /tmp/reload')
