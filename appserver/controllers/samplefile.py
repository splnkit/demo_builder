import logging
import os
import sys
import json
import cherrypy
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


class Samplefile(controllers.BaseController):
    ''' Samplefile Controller '''

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
        rsp_dict = {}     # os.listdir()
        rsp_dict["app"] = app
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
