# Copyright: (c) 2023, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import configparser

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: repo_info
author: Scott Harwell <sharwell@redhat.com>
short_description: Retrieves information about repositories managed by subscription manager.
version_added: "1.1.1"
description: Retrieves name, URL, and GPG key information about repositories managed by subscription manager.  This data can be used to populate TOML files for other tools, like Image Builder, to interact with these repositories.
options:
    repo:
        description: The repository that will be extracted from the repo file.
        required: True
    path:
        description:
            - Path to a different repository file
        type: string
        required: False
'''

EXAMPLES = r'''
# Pass in a repository
- name: Get Ansible repository info
  lab.composer.repo_info:
    name: ansible-automation-platform-2.4-for-rhel-9-x86_64-rpms

# Pass in a repository from a non-standard repo path
- name: Get Ansible repository info
  lab.composer.repo_info:
    name: ansible-automation-platform-2.4-for-rhel-9-x86_64-rpms
    path: /etc/yum.repos.d/epel.repo

# fail the module
- name: Test failure of the module
  lab.composer.repo_info:
    name: invalid_repo_name
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
repo:
    description: The repository requested.
    type: str
    returned: always
    sample: 'ansible-automation-platform-2.4-for-rhel-9-x86_64-rpms'
repo_file_path:
    description: The path of the repo file examined.
    type: str
    returned: always
    sample: '/etc/yum.repos.d/redhat.repo'
repo_response:
    description: The details of the repository returned.
    type: dict
    returned: always
    sample: {
            "baseurl": "https://cdn.redhat.com/content/dist/layered/rhel9/x86_64/ansible-automation-platform/2.4/os",
            "enabled": "1",
            "enabled_metadata": "1",
            "gpgcheck": "1",
            "gpgkey": "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release",
            "metadata_expire": "86400",
            "name": "Red Hat Ansible Automation Platform 2.4 for RHEL 9 x86_64 (RPMs)",
            "sslcacert": "/etc/rhsm/ca/redhat-uep.pem",
            "sslclientcert": "/etc/pki/entitlement/3766496840705121337.pem",
            "sslclientkey": "/etc/pki/entitlement/3766496840705121337-key.pem",
            "sslverify": "1",
            "sslverifystatus": "1"
        }
'''

def get_config_parser(path: str) -> configparser.ConfigParser:
    """Constructs a config parser object to part the file at the path provided.

    Args:
        path (str): A path on the filesystem to the repository file to read.

    Returns:
        configparser.ConfigParser: A config parser object.
    """

    abs_path = os.path.abspath(path)
    config = configparser.ConfigParser()
    config.read(abs_path)

    return config

def get_repo_data(config: configparser.ConfigParser, repo: str) -> {}:
    """Method to extract data from yum repository files.

    Args:
        config (ConfigParser): The config parser object to use.
        path (str): A path on the filesystem to the repository file to read.

    Returns:
        dict: A dictionary of key/value pairs with data about the repository.
    """

    items = config.items(repo)
    items = dict(items)

    output_repo = items

    return output_repo

def run_module():
    """The primary method called when running this Ansible module.
    """

    module_args = dict(
        repo=dict(type='str', required=True),
        path=dict(type='str', required=False, default='/etc/yum.repos.d/redhat.repo')
    )

    result = dict(
        changed=False,
        repo='',
        repo_file_path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    config = get_config_parser(module.params['path'])

    result['repo'] = module.params['repo']
    result['repo_file_path'] = module.params['path']
    result['repo_response'] = get_repo_data(config, module.params['repo'])
    result['changed'] = False

    module.exit_json(**result)

def main():
    """Main method called when script runs.
    """

    run_module()

if __name__ == '__main__':
    main()
