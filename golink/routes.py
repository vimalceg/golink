# aiohttpdemo_polls/routes.py
from golink import test1

def setup_routes(app):
    print("test",test1)
    app.router.add_get('/', test1.index)