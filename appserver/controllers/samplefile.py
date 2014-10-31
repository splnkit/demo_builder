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

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['GET'])
    def get(self, id='', action='get', **kwargs):
        '''Return list of files in "samples" directory'''
        pass

    @route('/:action')
    @expose_page(must_login=True, methods=['GET'])
    def list(self, id='', action='list', **kwargs):
        '''Return list of files in "samples" directory'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['POST'])
    def save(self, id='', action='save', **kwargs):
        '''Update a file in the "samples" directory'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['POST'])
    def create(self, id='', action='get', **kwargs):
        '''Create a file in the "samples" directory'''
        pass

    @route('/:id/:action')
    @expose_page(must_login=True, methods=['DELETE'])
    def delete(self, id='', action='get', **kwargs):
        '''Delete a file from the "samples" directory'''
        pass
