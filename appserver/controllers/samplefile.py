import logging
import os
import sys
import json
import cherrypy
import shutil
import cgi

from splunk.search import *
import splunk.appserver.mrsparkle.controllers as controllers
import splunk.appserver.mrsparkle.lib.util as util
from splunk.appserver.mrsparkle.lib.decorators import expose_page
from splunk.appserver.mrsparkle.lib.routes import route

dir = os.path.join(util.get_apps_dir(), __file__.split('.')[-2], 'bin')
if not dir in sys.path:
    sys.path.append(dir)

logger = logging.getLogger('splunk.appserver.controllers.samplefile')

appsDir = util.get_apps_dir()

CONFIG_URI = '/servicesNS/nobody/%s/eventgen/eventgen_conf'


def list_samplefiles(app=""):
    """Retreive a list of samplefiles for a given app context"""
    app_dir = os.path.join(appsDir, app, "samples")
    try:
        filename_list = [
            filename for filename in os.listdir(app_dir) if os.path.isfile(os.path.join(app_dir, filename))
        ]
    except OSError:
        return []
    return filename_list


def list_configs(app="", sessionKey=None):
    """Retreive a list of active configs for a given app context"""
    args = {'output_mode': 'json'}
    serverResponse, serverContent = splunk.rest.simpleRequest(
        CONFIG_URI % app,
        sessionKey=sessionKey,
        getargs=args
    )
    cherrypy.response.headers['Content-Type'] = 'text/json'
    content = json.loads(serverContent)
    filename_list = [
        filename["name"] for filename in content["entry"] if filename["acl"]["app"] == app
    ]
    return filename_list


def write_to_file(app="", id="", contents=""):
    if not os.path.isdir(os.path.join(appsDir, app, "samples")):
        os.mkdir(os.path.join(appsDir, app, "samples"))
    open(os.path.join(appsDir, app, "samples", id)).write(contents)


# replay
def write_job_contents(sid="", app="", id="", sessionKey=None, mode="sample"):
    job = getJob(sid=sid, sessionKey=sessionKey)
    try:
        ofile = open(os.path.join(appsDir, app, "samples", id), "w")
    except IOError:
        os.mkdir(os.path.join(appsDir, app, "samples"))
        ofile = open(os.path.join(appsDir, app, "samples", id), "w")
    results = job.results
    if mode == "replay":
        cw = csv.DictWriter(ofile, results.fieldOrder[:-1])
        cw.writeheader()
        for result in results:
            cw.writerow(result)
    else:
        for result in results:
            ofile.write("%s\n" % result)
    ofile.close()


def processFileUpload(f, app="", id=""):
    """
    Process a file uploaded from the upload page
    """
    if not (isinstance(f, cgi.FieldStorage) and f.file):
        return
    tfile = open(os.path.join(appsDir, app, "samples", id), "w+")
    shutil.copyfileobj(f.file, tfile)
    tfile.close()
    return


class Samplefile(controllers.BaseController):
    ''' Samplefile Controller '''

    @route('/:app/:action=index')
    @expose_page(must_login=True, methods=['GET'])
    def index(self, app='', action='index', **kwargs):
        '''Return list of files in "samples" directory'''
        rsp_dict = {}
        rsp_dict["app"] = app
        sample_files = set(list_samplefiles(app=app))
        configs = set(list_configs(app=app))
        rsp_dict["files"] = list(configs - sample_files)
        rsp_dict["configs"] = list(configs & sample_files)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        return json.dumps(rsp_dict)

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['GET'])
    def get(self, app='', id='', action='get', **kwargs):
        '''Return list of files in "samples" directory'''
        file_path = os.path.join(appsDir, app, "samples", id)
        rsp_dict = {}
        rsp_dict["app"] = app
        rsp_dict["filename"] = id
        rsp_dict["content"] = open(file_path, "r").read()
        cherrypy.response.headers['Content-Type'] = 'text/json'
        return json.dumps(rsp_dict)

    @route('/:app/:action=list')
    @expose_page(must_login=True, methods=['GET'])
    def list(self, app='', action='list', **kwargs):
        '''Return list of files in "samples" directory'''
        session_key = cherrypy.session.get('sessionKey')  # to delete
        rsp_dict = {}     # os.listdir()
        rsp_dict["app"] = app
        rsp_dict["key"] = session_key   # to delete
        app_dir = os.path.join(appsDir, app, "samples")
        filename_list = [
            filename for filename in os.listdir(app_dir) if os.path.isfile(os.path.join(app_dir, filename))
        ]
        rsp_dict["files"] = filename_list
        cherrypy.response.headers['Content-Type'] = 'text/json'
        return json.dumps(rsp_dict)

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['POST', 'PUT'])
    def save(self, app='', id='', action='save', **kwargs):
        '''Update a file in the "samples" directory'''
        file_path = os.path.join(appsDir, app, "samples", id)
        open(file_path, "w").write(kwargs["contents"])
        return json.dumps({"Status": 200, "Message": "File written."})

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['DELETE'])
    def delete(self, app='', id='', action='delete', **kwargs):
        '''Delete a file from the "samples" directory'''
        file_path = os.path.join(appsDir, app, "samples", id)
        os.remove(file_path)
        return json.dumps({"Status": 200, "Message": "File deleted."})

    @route('/:app/:id/:action=saveresults')
    @expose_page(must_login=True, methods=['DELETE'])
    def search(self, app='', id='', action='delete', **kwargs):
        '''Save the search results to a file in the "samples" directory'''
        session_key = cherrypy.session.get('sessionKey')
        sid = kwargs.get("sid")
        mode = kwargs.get("mode")
        write_job_contents(sid=sid, app=app, id=id, sessionKey=session_key, mode=mode)
        return json.dumps({"Status": 200, "Message": "Results saved to file."})

    @route('/:app/:id/:action=_upload')
    @expose_page(must_login=True, methods=['GET', 'POST'])
    def upload(self, app, id="", file=None, force=None, **kwargs):
        """
        Present a form for direct upload of an app
        """
        if file is not None and cherrypy.request.method == 'POST':
            cherrypy.response.headers['Content-Type'] = 'text/json'
            try:
                processFileUpload(file, app=app, id=id)
                return json.dumps({"Status": 200, "Message": "File uploaded successfully."})
            except:
                return json.dumps({"Status": 500, "Message": "File could not be uploaded."})
        else:
            return self.render_template('/demo_builder:/templates/setup_show.html', dict())
