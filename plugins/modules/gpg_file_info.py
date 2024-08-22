# Copyright: (c) 2023, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: gpg_file_info
author: Scott Harwell <sharwell@redhat.com>
short_description: Retrieves GPG keys from files on Linux systems.
version_added: "1.1.2"
description: Parses GPG files into individual keys.
options:
    path:
        description: Path to a file to read GPG keys from.
        type: string
        required: True
'''

EXAMPLES = r'''
# Get GPG keys from file at path
- name: Get gpg keys from file
  lab.composer.gpg_file_info:
    path: /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
path:
    description: The path of the file requested
    type: str
    returned: always
    sample: /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
gpg_keys:
    description: An array of GPG keys found in the file.
    type: arr
    returned: always
    sample: []
'''

def get_file(path: str) -> str:
    """Gets the data from a file as a string.

    Args:
        path (str): The path to the file to read.

    Returns:
        str: The contents of the file as a string.
    """

    with open(path, "r+", encoding='UTF8') as file:
        return file.read()

def parse_keys(file_data: str) -> []:
    """Parses the contents of a string into one or more GPG keys.

    Args:
        file_data (str): The string data to parse.

    Returns:
        []: The array of GPG keys parsed from the original string.
    """    

    keys = []
    split = file_data.split('-----BEGIN')

    for item in split:
        if "-----END" in item:
            key = f"-----BEGIN{item}".strip()
            keys.append(key)

    return keys

def run_module():
    """The primary method called when running this Ansible module.
    """

    module_args = dict(
        path=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    file_data = get_file(module.params['path'])
    keys = parse_keys(file_data)

    result['path'] = module.params['path']
    result['gpg_keys'] = keys
    result['changed'] = False

    module.exit_json(**result)

def main():
    """Main method called when script runs.
    """

    run_module()

if __name__ == '__main__':
    main()
