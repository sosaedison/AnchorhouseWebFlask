from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)
from anchorwebflask import routes