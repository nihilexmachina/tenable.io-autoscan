import os

def get_env_vars():
    env_vars = {}
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            env_vars[key] = value
    return env_vars

def write_target_group_ids_and_names(env_vars):
    target_group_ids_and_names = []
    for key, value in env_vars.items():
        if key.startswith("TARGET_GROUP_"):
            target_group_id = key.replace("TARGET_GROUP_", "")
            target_group_name = value
            target_group_ids_and_names.append((target_group_id, target_group_name))
    with open("target_group_ids_and_names.txt", "w") as f:
        for target_group_id, target_group_name in target_group_ids_and_names:
            f.write(f"{target_group_id}: {target_group_name}\n")

def write_key_fields(env_vars):
    key_fields = []
    for key in env_vars.keys():
        if not key.startswith("TARGET_GROUP_"):
            key_fields.append(key)
    with open("key_fields.txt", "w") as f:
        for key_field in key_fields:
            f.write(f"{key_field}\n")

if __name__ == "__main__":
    env_vars = get_env_vars()
    write_target_group_ids_and_names(env_vars)
    write_key_fields(env_vars)
