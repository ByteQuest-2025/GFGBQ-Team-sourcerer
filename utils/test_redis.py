import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_all_keys_and_values():
    """
    Fetch all keys and their values from Redis safely.
    """
    result = {}

    cursor = 0
    while True:
        cursor, keys = r.scan(cursor)
        for key in keys:
            key_type = r.type(key)

            if key_type == "string":
                value = r.get(key)

            elif key_type == "list":
                value = r.lrange(key, 0, -1)

            elif key_type == "hash":
                value = r.hgetall(key)

            elif key_type == "set":
                value = list(r.smembers(key))

            elif key_type == "zset":
                value = r.zrange(key, 0, -1, withscores=True)

            else:
                value = "<unsupported type>"

            result[key] = {
                "type": key_type,
                "value": value,
                "ttl": r.ttl(key)
            }

        if cursor == 0:
            break

    return result


if __name__ == "__main__":
    data = get_all_keys_and_values()

    for key, info in data.items():
        print(f"\nKEY: {key}")
        print(f"TYPE: {info['type']}")
        print(f"TTL : {info['ttl']}")
        print(f"VALUE:\n{info['value']}")
