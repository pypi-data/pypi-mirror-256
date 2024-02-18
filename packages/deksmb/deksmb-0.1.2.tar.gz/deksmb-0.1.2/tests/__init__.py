from deksmb.client.base import SmbClient

if __name__ == '__main__':
    client = SmbClient('192.168.11.103', 'zzz', username='node', password='123456')
    client.connect()
    client.download_dir('/test', '.')
