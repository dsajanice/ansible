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
        required: false
        type: bool
        default: 'no'
    update_runtime:
        description:
            - Updates iotedged runtime components to latest or specified version
        required: false
        suboptions:
          description:
            - Version of iotedged runtime components to update to
          version: str
          required: false
          default: 'latest' 

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

# Update iotedged runtime components to latest
- name: Update iotedged runtime components
  azure_rm_iotedge:
    update_runtime:

# Update iotedged runtime components to 1.0.6
- name: Update iotedged runtime components to 1.0.6
  azure_rm_iotedge:
    update_runtime:
      version: 1.0.6

# Conditional update of iotedged runtime components
- name: Update iotedged runtime components to 1.0.6 if current version is different
  azure_rm_iotedge:
    version: yes
  register: version_info 
    update_runtime:
      version: 1.0.6
  when: version_info.version != "1.0.6"

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

class UpdateRuntimeCommand(object):
    def __init__(self, desired):
        self.desired = desired
        return

    def execute(self):
        print('Updating Azure IoT Edge runtime components to {}'.format(self.desired))
        if self.desired == 'latest':
          out = subprocess.Popen(['apt-get', 'install', '-y', 'iotedge']),
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT)
        else:
          package = 'iotedge=' + self.desired
          out = subprocess.Popen(['apt-get', 'install', '-y', '--allow-downgrades', package]),
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT)
        return

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        version=dict(type='bool', default=False),
        update_runtime=dict(type='list', elements='dict', options=dict(
            version=dict(type='str', default='latest'),
        ))
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        version=''
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

    if module.params['update_runtime']:
      version = module.params['update_runtime'][0].get('version')
      cmd = UpdateRuntimeCommand(version)
      cmd.execute()

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
