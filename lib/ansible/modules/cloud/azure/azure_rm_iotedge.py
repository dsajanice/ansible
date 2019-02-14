#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: azure_rm_iotedge

short_description: This module is used to manage an Azure IoT Edge device from the cloud

version_added: "1.0"

description:
    - "This is my Azure IoT Edge module"

options:
    version:
        description:
            - Retrieves the version of iotedged on the device

extends_documentation_fragment:
    - azure

author:
    - Janice D'Sa (@dsajanice)
'''

EXAMPLES = '''
# Get installed iotedged version from device
- name: Get installed iotedged version
  azure_rm_iotedge:
    version: yes
'''

RETURN = '''
azure_rm_iotedge:
    description: Returns command output if any
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

class VersionCommand(object):
    def __init__(self):
        return

    def execute(self):
        out = subprocess.Popen(['iotedge', '--version'],
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        print(stdout)
        return stdout.split()[1]

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        version=dict(type='bool', default=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    #result['original_message'] = module.params['name']
    #result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['version']:
      cmd = VersionCommand()
      version = cmd.execute()
      result['changed'] = False
      result['version'] = version

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
