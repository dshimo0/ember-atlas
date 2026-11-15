"""Serve the static site with the same explicit route fallbacks as Vercel."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]/'web'
class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        if urlsplit(path).path.rstrip('/') in ['/demo','/pitch']:
            return str(ROOT/'index.html')
        return super().translate_path(path)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--bind',default='127.0.0.1');a=p.parse_args()
    ThreadingHTTPServer((a.bind,a.port),partial(Handler,directory=str(ROOT))).serve_forever()
