import typer
from ..client.base import SmbClient
from getpass import getpass

app = typer.Typer(add_completion=False)


@app.command()
def send(username, host, share, src, dest):
    password = getpass()
    client = SmbClient(host, share, username=username, password=password)
    client.connect()
    if client.is_file(src):
        client.download(src, dest)
    else:
        client.download_dir(src, dest)
