from convergence.convergence_service import ConvergenceService, ConvergenceEndpointRateLimitPolicy


def __convert_size_to_bytes(max_payload_size: str):
    coeff = 0
    if max_payload_size.endswith("KB"):
        coeff = 1024
    elif max_payload_size.endswith("MB"):
        coeff = 1024 * 1024
    elif max_payload_size.endswith("GB"):
        coeff = 1024 * 1024 * 1024
    else:
        raise ValueError(f'The value {max_payload_size} is not valid.')

    value = int(max_payload_size[0:-2])
    return coeff * value


def __convert_time_out_to_ms(timeout: str):
    value = 0
    if timeout.endswith("ms"):
        value = int(timeout[0:-2])
    elif timeout.endswith("s"):
        value = 1000 * int(timeout[0:-1])
    else:
        raise ValueError(f'The value {timeout} is not valid.')

    return value


def __parse_rate_limiting_policies(rate_limiting_policy):
    if rate_limiting_policy is None:
        return []

    result = []
    for p in rate_limiting_policy:
        parts = p.split(":")
        if len(parts) != 3:
            raise ValueError(f'The value {p} is not a valid rate limiting policy.')

        if parts[0] not in ['max_globally', 'max_per_session', 'max_per_ip']:
            raise ValueError(f'The value {p} is not a valid rate limiting policy.')

        c = ConvergenceEndpointRateLimitPolicy()
        c.policy = parts[0]
        c.count = int(parts[1])

        duration = parts[2]
        coeff = 0
        units = {
            's': 1,
            'm': 60,
            'h': 3600
        }

        valid_unit = False
        for k, v in units.items():
            if duration.endswith(k):
                valid_unit = True
                coeff = v

        if not valid_unit:
            raise ValueError(f'The value {p} is not a valid rate limiting policy.')

        value = int(duration[0:-1]) * coeff
        c.duration = value
        result.append(c)

    return result


def __validate_maintenance_mode(maintenance_mode):
    if maintenance_mode not in ['allow', 'restrict']:
        raise ValueError(f'The value {maintenance_mode} is not valid.')


def convergence_endpoint(router, url,
                         method='GET',
                         exposed_through_gateway=True,
                         authorization=None,
                         max_payload_size='200KB',
                         timeout='10s',
                         rate_limiting_policy=None,
                         maintenance_mode='restrict',
                         accepts=['application/json']):
    max_payload_size = __convert_size_to_bytes(max_payload_size)
    timeout = __convert_time_out_to_ms(timeout)
    rate_limiting_policy = __parse_rate_limiting_policies(rate_limiting_policy)
    __validate_maintenance_mode(maintenance_mode)

    ConvergenceService.register_endpoint_info(url,
                                              method,
                                              authorization,
                                              exposed_through_gateway,
                                              max_payload_size,
                                              timeout,
                                              rate_limiting_policy,
                                              maintenance_mode,
                                              accepts)

    def wrapper(func):
        if method.upper() == 'GET':
            router.get(url)(func)
        elif method.upper() == 'POST':
            router.post(url)(func)
        elif method.upper() == 'PUT':
            router.put(url)(func)
        elif method.upper() == 'PATCH':
            router.patch(url)(func)
        elif method.upper() == 'DELETE':
            router.delete(url)(func)

        return func

    return wrapper
