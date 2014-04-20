# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


@app.route('/movies')
def movies():
	return render_template('movies/master.html')

@app.route('/movies/<movieId>')
def movie_item(movieId):
    return render_template('movies/movie.html')