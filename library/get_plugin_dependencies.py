#!/usr/bin/python


from ansible.module_utils.basic import *  # NOQA
import json
from os.path import basename


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(
                type='str',
                required=True),
            deployment_ssh_key=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/.ssh/id_rsa'),
            cli_path=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/jenkins-cli.jar'),
            groovy_scripts_path=dict(
                type='str',
                required=False,
                default='/var/lib/jenkins/groovy_scripts'),
            url=dict(
                type='str',
                required=False,
                default='http://localhost:8080')
        )
    )

    script = "%s/%s.groovy" % (module.params['groovy_scripts_path'],
                               basename(__file__))

    rc, stdout, stderr = module.run_command(
        "java -jar %s -s '%s' -i '%s' groovy %s %s" %
        (module.params['cli_path'], module.params['url'],
         module.params['deployment_ssh_key'], script,
         module.params['name']))

    if (rc != 0):
        module.fail_json(msg=stderr)

    json_stdout = json.loads(stdout)
    module.exit_json(changed=bool(json_stdout), output=json_stdout)


if __name__ == '__main__':
    main()
