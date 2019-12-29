#!/usr/bin/python3
from flask import Flask, render_template, make_response, request, jsonify, \
    redirect, send_from_directory
from flask_caching import Cache
import requests
import os
import tempfile
from conversion import convert_json_to_ics

# configuration
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
PORT = int(os.environ.get("PORT", "5000"))
CACHE_REQUESTED_URLS_FOR_SECONDS = int(os.environ.get(
    "CACHE_REQUESTED_URLS_FOR_SECONDS", 
    (1 if DEBUG else 600)))
# the source url can be retrieved from the wiki page
# https://events.ccc.de/congress/2019/wiki/index.php/Static:Schedule#Merged_schedules_.28XML_.2F_JSON.29
SOURCE_JSON_URL = "https://data.c3voc.de/36C3/everything.schedule.json"

# globals
app = Flask(__name__, template_folder="templates")
# Check Configuring Flask-Cache section for more details
cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': tempfile.mktemp(prefix="cache-")})

def set_JS_headers(response):
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
    response.headers['Access-Control-Allow-Headers'] = request.headers.get("Access-Control-Request-Headers")
    response.headers['Content-Type'] = 'text/calendar'
    return response

def set_js_headers(func):
    """Set the response headers for a valid CORS request."""
    def with_js_response(*args, **kw):
        return set_JS_headers(func(*args, **kw))
    return with_js_response

@app.route("/36c3.ics", methods=['GET', 'OPTIONS'])
# use query string in cache, see https://stackoverflow.com/a/47181782/1320237
@cache.cached(timeout=CACHE_REQUESTED_URLS_FOR_SECONDS, query_string=True)
@set_js_headers
def get_calendar():
    """Return a calendar."""
    source = requests.get(SOURCE_JSON_URL)
    data = source.json()
    ics = convert_json_to_ics(data)
    return ics.to_ical()
    
@app.errorhandler(500)
def unhandledException(error):
    """Called when an error occurs.

    See https://stackoverflow.com/q/14993318
    """
    file = io.StringIO()
    traceback.print_exception(type(error), error, error.__traceback__, file=file)
    return """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <html>
        <head>
            <title>500 Internal Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>
            <pre>\r\n{traceback}
            </pre>
        </body>
    </html>
    """.format(traceback=file.getvalue()), 500 # return error code from https://stackoverflow.com/a/7824605

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)

