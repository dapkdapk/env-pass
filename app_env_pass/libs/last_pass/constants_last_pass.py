TMPL_ENV_FILE = """declare -a vars=({env_vars})
pass_to_get=0
if ! $(lpass ls > /dev/null 2>&1)
then
    echo "Logging into last pass..." 
    echo -n "LastPass username: "
    read username
    lpass login $username
    pass_to_get=1
else
    echo "Valid last pass login found."
    lpass status
    pass_to_get=1
fi

if [[ "$pass_to_get" == 1 ]]; then
    lines=$(lpass show {id})
    #export USERNAME="$(echo "$lines" | grep '^Username:' | cut -d' ' -f2)"
    {export_list}
fi
"""

TMPL_EXPORT_ITEM = '''export {env_name}="$(echo "$lines" | grep '^{key_name}:' | cut -d' ' -f2)"'''

DEFAULT_ENV_FILE_OUTPUT = "./sample_last_pass.env"
