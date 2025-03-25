
from flask import *
import json
import main

serv=Flask(__name__)

@serv.route('/search')
def serc():
    user = request.args.get('id')
    return main.process_id(user)

if __name__ == "__main__":
    serv.run()