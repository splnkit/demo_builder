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

logger = logging.getLogger('splunk.appserver.controllers.eventgen')

appsDir = util.get_apps_dir()


class Eventgen(controllers.BaseController):
    ''' Eventgens Controller '''

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['GET'])
    def get(self, id='', action='get', **kwargs):
        '''Return list of eventgen configs'''
        pass

    @route('/:action')
    @expose_page(must_login=True, methods=['GET'])
    def list(self, id='', action='list', **kwargs):
        '''Return list of eventgen configs'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['POST'])
    def save(self, id='', action='save', **kwargs):
        '''Update an eventgen config'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['POST'])
    def create(self, id='', action='get', **kwargs):
        '''Create a new eventgen config'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['DELETE'])
    def delete(self, id='', action='get', **kwargs):
        '''Delete an eventgen config'''
        pass
