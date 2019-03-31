#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from lahacks_hack import query_api
app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'weather.html')



@app.route('/result', methods=['POST'])
def result():
	error= None
	a,d,j,n,o,wor,magnitude,score,speed=query_api()

	return render_template('result.html',a=a,d=d,j=j,n=n,o=o,wor=wor,magnitude=magnitude,score=score,speed=speed,error=error)

 
    
    
if __name__=='__main__':
    app.run(debug=True)

