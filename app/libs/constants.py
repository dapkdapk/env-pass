OBJ_KEY_TMP = "obj"

TMPL_ENV_FILE = """declare -a vars=({env_vars})
pass_to_get=0
if ! $(pass-cli info -o json | jq '.username' > /dev/null 2>&1)
then
        echo "Logging into proton pass..."
        pass-cli login
        pass_to_get=1
else
        echo "Valid proton pass token found."
        pass_to_get=1
fi

if [[ "$pass_to_get" == 1 ]]; then
        json=$(pass-cli item view --output json --share-id {shared_id} --item-id {item_id})
        {export_list}
fi
"""
TMPL_EXPORT_ITEM = '''export {env_name}="$(echo $json | jq -Rnr '[inputs] | join("") | fromjson | .{json_path}')"'''
TMPL_EXPORT_ITEM_LIST = '''export {env_name}="$(echo $json | jq -Rnr '[inputs] | join("") | fromjson | .{json_path} | select(.name == "{name}") | .content.Text')"'''
DEFAULT_ENV_FILE_OUTPUT = "./sample.env"
