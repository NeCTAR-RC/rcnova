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
import base64

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


class ProjectAdminController(object):

    def show(self, req, id):
        return project_dict(auth_manager.AuthManager().get_project(id))

    def index(self, req):
        user_id = getattr(req.environ['nova.context'], 'user_id', '')
        project_id = getattr(req.environ['nova.context'], 'project_id', '')
        return {"project-zip": 
                base64.encodestring(auth_manager.AuthManager().get_credentials(user_id, project_id))}


class ProjectAdmin(object):

    def __init__(self):
        pass

    def get_name(self):
        return "Project Admin Controller"

    def get_alias(self):
        return "NECTAR-PROJECT"

    def get_description(self):
        return "A Project Admin API Extension"

    def get_namespace(self):
        return "http://nectar.org.au"

    def get_updated(self):
        return "2011-05-25 16:12:21.656723"

    def get_resources(self):
        resources = []
        resources.append(extensions.ResourceExtension('test/',
                                                 AdminProjectController()))
        return resources
