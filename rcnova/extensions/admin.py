# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nectar Project
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from webob import exc

from nova import db
from nova.auth import manager as auth_manager
from nova.api.openstack import extensions
from nova.api.openstack import wsgi


LOG = logging.getLogger('rcnova.extensions.admin')


def project_dict(project):
    """Convert the project object to a result dict"""
    if project:
        return {
            'id': project.id,
            'name': project.id,
            'projectname': project.id,
            'project_manager_id': project.project_manager_id,
            'description': project.description}
    else:
        return {}


class AdminProjectController(object):

    def show(self, req, id):
        return project_dict(auth_manager.AuthManager().get_project(id))

    def index(self, req):
        user_id = getattr(req.environ['nova.context'], 'user_id', '')
        project_id = getattr(req.environ['nova.context'], 'project_id', '')
        return auth_manager.AuthManager().get_credentials(user_id, project_id)

    def create(self, req, body):
        name = body['project'].get('name')
        manager_user = body['project'].get('manager_user')
        description = body['project'].get('description')
        member_users = body['project'].get('member_users')

        context = req.environ['nova.context']
        msg = _("Create project %(name)s managed by"
                " %(manager_user)s") % locals()
        LOG.audit(msg, context=context)
        project = project_dict(
                     auth_manager.AuthManager().create_project(
                     name,
                     manager_user,
                     description=None,
                     member_users=None))
        return {'project': project}

    def update(self, req, id, body):
        context = req.environ['nova.context']
        name = id
        manager_user = body['project'].get('manager_user')
        description = body['project'].get('description')
        msg = _("Modify project: %(name)s managed by"
                " %(manager_user)s") % locals()
        LOG.audit(msg, context=context)
        auth_manager.AuthManager().modify_project(name,
                                             manager_user=manager_user,
                                             description=description)
        return exc.HTTPAccepted()

    def delete(self, req, id):
        context = req.environ['nova.context']
        LOG.audit(_("Delete project: %s"), id, context=context)
        auth_manager.AuthManager().delete_project(id)
        return exc.HTTPAccepted()


class BinarySerializer(wsgi.DictSerializer):
    """Default JSON request body serialization"""

    def default(self, data):
        raise Exception('test')
        return data


class Admin(object):

    def __init__(self):
        pass

    def get_name(self):
        return "Admin Controller"

    def get_alias(self):
        return "ADMIN"

    def get_description(self):
        return "The Admin API Extension"

    def get_namespace(self):
        return "http:TODO/"

    def get_updated(self):
        return "2011-05-25 16:12:21.656723"

    def get_resources(self):
        resources = []
        body_serializers = {'application/zip': BinarySerializer()}
        serializer = wsgi.ResponseSerializer(body_serializers)
        del serializer.body_serializers['application/xml']
        del serializer.body_serializers['application/json']
        resources.append(extensions.ResourceExtension('test/',
                                                 AdminProjectController(),
                                                 serializer=serializer))
        return resources
