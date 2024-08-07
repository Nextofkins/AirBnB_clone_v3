#!/usr/bin/python3
""" 
Creating a flask app; app_views
"""
from flask import jsonfy
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """
    
    """
    response = {'status': "OK"}
    return jsonfy(response)