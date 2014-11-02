import logging
import os
import sys
import json
import cherrypy
import splunk
from splunk.search import *
import splunk.appserver.mrsparkle.controllers as controllers
import splunk.appserver.mrsparkle.lib.util as util
from splunk.appserver.mrsparkle.lib.decorators import expose_page
from splunk.appserver.mrsparkle.lib.routes import route

dir = os.path.join(util.get_apps_dir(), __file__.split('.')[-2], 'bin')
if not dir in sys.path:
    sys.path.append(dir)

logger = logging.getLogger('splunk.appserver.controllers.eventgen')

appsDir = util.get_apps_dir()


class Eventgen(controllers.BaseController):
    ''' Eventgens Controller '''

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['GET'])
    def get(self, app='', id='', action='get', **kwargs):
        '''Return list of eventgen configs'''
        session_key = cherrypy.session.get('sessionKey')
        args = kwargs
        args['output_mode'] = 'json'
        serverResponse, serverContent = splunk.rest.simpleRequest('/services/eventgen/eventgen_conf/%s' % id, sessionKey=session_key, getargs=args)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        content = json.loads(serverContent)["entry"][0]["content"]
        return json.dumps(content)

    @route('/:app/:action=list')
    @expose_page(must_login=True, methods=['GET'])
    def default(self, app='', **kwargs):
        '''Return list of eventgen configs'''
        session_key = cherrypy.session.get('sessionKey')
        args = {}
        args['output_mode'] = 'json'
        serverResponse, serverContent = splunk.rest.simpleRequest('/services/eventgen/eventgen_conf', sessionKey=session_key, getargs=args)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        #content = json.loads(serverContent)["entry"][0]["content"]
        return serverContent

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['POST', 'PUT'])
    def save(self, app='', id='', action='save', **kwargs):
        '''Update an eventgen config'''
        session_key = cherrypy.session.get('sessionKey')
        args = {}
        args['output_mode'] = 'json'
        serverResponse, serverContent = splunk.rest.simpleRequest('/services/eventgen/eventgen_conf/%s' % id, sessionKey=session_key, postargs=args)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        #content = json.loads(serverContent)["entry"][0]["content"]
        return serverContent

    @route('/:app/:id/:action')
    @expose_page(must_login=True, methods=['POST'])
    def create(self, app='', id='', action='create', **kwargs):
        '''Create a new eventgen config'''
        session_key = cherrypy.session.get('sessionKey')
        args = kwargs
        args['output_mode'] = 'json'
        serverResponse, serverContent = splunk.rest.simpleRequest('/services/eventgen/eventgen_conf/%s' % id, sessionKey=session_key, postargs=args)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        #content = json.loads(serverContent)["entry"][0]["content"]
        return serverContent

    @route('/:app/:id/:action=delete')
    @expose_page(must_login=True, methods=['GET'])
    def delete(self, app='', id='', action='delete', **kwargs):
        '''Delete an eventgen config'''
        session_key = cherrypy.session.get('sessionKey')
        args = {}
        args['output_mode'] = 'json'
        serverResponse, serverContent = splunk.rest.simpleRequest('/services/eventgen/eventgen_conf/%s' % id, sessionKey=session_key, method='DELETE', getargs=args)
        cherrypy.response.headers['Content-Type'] = 'text/json'
        return serverContent
