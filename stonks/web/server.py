from flask import Flask, request, redirect
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
from flask_cors import CORS
from json import dumps, loads
from datetime import datetime
from hashlib import md5
from random import randint
from ..web.logsaver import LogSaver
import threading
from absl import logging


def StartServer():
    # Initialize flask app and api
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    ls = LogSaver()

    # classes responsible for request handling

    class GetBalance(Resource):
        def get(self):
            args = get_parser.parse_args()
            if args['time'] is None:
                return {'message': 'No timestamp provided'}, 400
            return jsonify(
                {
                    'message': f'sending logs from {args["time_start"]} to {args["time_finish"]}',
                    'data': ls.GetBalance(args['time_start'], args['time_finish'])
                }
            )

    class GetDeals(Resource):
        def get(self):
            args = get_parser.parse_args()
            if args['time'] is None:
                return {'message': 'No timestamp provided'}, 400
            return jsonify(
                {
                    'message': f'sending logs from {args["time_start"]} to {args["time_finish"]}',
                    'data': ls.GetDealsAmountDict()
                }
            )

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('time_start')
    get_parser.add_argument('time_finish')

    api.add_resource(GetBalance, '/api/balance')
    api.add_resource(GetDeals, '/api/deals')

    flask_thread = threading.Thread(
        target=app.run, kwargs={
            'debug': True,
            'use_reloader': False,
            'port': 5000,
            'host': '0.0.0.0'
        }
    )
    flask_thread.start()