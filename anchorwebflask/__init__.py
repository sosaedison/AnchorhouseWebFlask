from flask import Flask, render_template, url_for, redirect
application = Flask(__name__)
from anchorwebflask import routes