from http.cookiejar import debug

from flask import *

serv=Flask(__name__)

@serv.route('/')
def first_page():
    return "It is first page"

if __name__ == "__main__":
    serv.run(debug=True)