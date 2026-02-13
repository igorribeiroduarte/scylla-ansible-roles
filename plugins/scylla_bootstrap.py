from ansible.module_utils.basic import AnsibleModule


class SystemCtl:
    @staticmethod
    def get_service_status(module, service_name: str):
        args = ["is-active", service_name]
        rc, out, err = module.run_command(['systemctl'] + args, check_rc=False)

        return rc, out, err

    def is_service_started(module, service_name: str):
        args = ["is-active", service_name]
        rc, out, err = module.run_command(['systemctl'] + args, check_rc=False)

        return rc == 0

    @staticmethod
    def start_service(module, service_name: str):
        args = ["start", service_name]
        rc, out, err = module.run_command(['systemctl'] + args, check_rc=False)

        return rc, out, err


def run_module():
    module_args = dict(
        timeout = dict(type='int', required=True),
        rpc_address = dict(type='str', required=True)
    )

    result = dict(changed=False, original_message='', message='')


    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        changed = not SystemCtl.is_service_started(module, 'scylla-server')
        module.exit_json(changed=changed)

    rc, out, err = SystemCtl.start_service(module, 'scylla-server')

    if rc != 0:
        result['original_message'] = out
        result['message'] = err 

        module.fail_json(msg="Failed to start service", **result)


    # Execute the bootstrap

    #rc, out, err = module.run_command(['systemctl', 'status', 'scylla-server'], check_rc=True)
    #result['original_message'] = out + err

    #if rc == 0:
    #    # succeeded
    #    pass
    #else:
    #    # failed
    #    pass

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
