import logging
import copy
import splunk
import splunk.admin as admin
import splunk.entity as en

logger = logging.getLogger('splunk')

required_args = ['bang']
optional_args = ['disabled', 'has_ignored', 'introspect']
acl_args = ['owner', 'sharing']

ENDPOINT = 'configs/conf-eventgen'


class EventgenHandler(admin.MConfigHandler):

    def setup(self):

        if self.requestedAction not in [admin.ACTION_LIST, admin.ACTION_REMOVE]:
            for arg in required_args:
                self.supportedArgs.addReqArg(arg)

            for arg in optional_args:
                self.supportedArgs.addOptArg(arg)

            for arg in self.callerArgs:
                self.supportedArgs.addOptArg(arg)

    def handleList(self, confInfo):

        ent = en.getEntities(ENDPOINT,
                             namespace=self.appName,
                             owner=self.userName,
                             sessionKey=self.getSessionKey())

        for name, obj in ent.items():
            confItem = confInfo[name]
            for key, val in obj.items():
                confItem[key] = str(val)
            acl = {}
            for k, v in obj[admin.EAI_ENTRY_ACL].items():
                if None != v:
                    acl[k] = v
            confItem.setMetadata(admin.EAI_ENTRY_ACL, acl)

    def handleEdit(self, confInfo):
        name = self.callerArgs.id

        ent = en.getEntity(ENDPOINT, name,
                           namespace=self.appName,
                           owner=self.userName,
                           sessionKey=self.getSessionKey())

        for arg in optional_args:
            try:
                if arg in ['disabled']:
                    continue
                ent[arg] = self.callerArgs[arg]
            except:
                pass

        for arg in required_args:
            try:
                if arg in ['disabled']:
                    continue
                ent[arg] = self.callerArgs[arg]
            except:
                pass

        en.setEntity(ent, sessionKey=self.getSessionKey())

    def handleCreate(self, confInfo):

        name = self.callerArgs.id

        new = en.Entity(ENDPOINT, name,
                        namespace=self.appName, owner=self.userName)

        for arg in required_args:
            new[arg] = self.callerArgs[arg]

        for arg in self.callerArgs:
            if arg in ['disabled']:
                continue
            try:
                new[arg] = self.callerArgs[arg]
            except:
                pass

        en.setEntity(new, sessionKey=self.getSessionKey())

        self.callerArgs.data = {"owner": "nobody", "sharing": "global"}
        self.handleACL(confInfo)

    def handleRemove(self, confInfo):

        name = self.callerArgs.id

        en.deleteEntity(ENDPOINT, name,
                        namespace=self.appName,
                        owner=self.userName,
                        sessionKey=self.getSessionKey())

    def handleCustom(self, confInfo):
        if self.customAction in ['acl']:
            return self.handleACL(confInfo)

    def handleACL(self, confInfo):
        try:
            ent = self.get()
            meta = ent[admin.EAI_ENTRY_ACL]

            if self.requestedAction in [admin.ACTION_CREATE, admin.ACTION_EDIT] and len(self.callerArgs.data) > 0:

                ent.properties = dict()

                ent['sharing'] = meta['sharing']
                ent['owner'] = meta['owner']

                ent['perms.read'] = ['*']
                ent['perms.write'] = ['*']

                ent["owner"] = "nobody"
                ent["sharing"] = "global"

                en.setEntity(ent, self.getSessionKey(), uri=ent.id + '/acl')
                ent = self.get()

            confItem = confInfo[self.callerArgs.id]
            acl = copy.deepcopy(meta)
            confItem.actions = self.requestedAction
            confItem.setMetadata(admin.EAI_ENTRY_ACL, acl)

        except splunk.ResourceNotFound as ex:
            logger.exception('handleACL Failed - arguments = %s, exception = %s' % (self.callerArgs, ex))

    def get(self):
        app, user = self._namespace_and_owner()

        return en.getEntity(self._endpoint,
                            self.callerArgs.id,
                            namespace=app,
                            owner=user,
                            sessionKey=self.getSessionKey())

    @property
    def _endpoint(self):
        return ENDPOINT

    def _namespace_and_owner(self):
        app = self.appName
        user = self.userName
        return app, user

admin.init(EventgenHandler, admin.CONTEXT_APP_ONLY)
