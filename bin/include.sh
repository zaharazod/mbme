export ops=(venv force pip help upgrade npm db files)
export run=()

setting() {
    x=$1
    echo "
from config import config
parts = '$x'.split('.')
ctx = config.settings
while len(parts):
    part = parts.pop(0)
    if isinstance(ctx, dict):
        ctx = ctx.get(part, {})
    else:
        break
print(ctx)
    " | python
}

op() {
    srch=$1
    echo "${ops[@]}" | grep "$srch" 
    return $?
}

op2() {
    local -n enabled="$run"
    srch=()
    srch+=($1)
    echo "run: ${enabled[@]}"
    echo "srch: ${srch[@]}"
    while shift; do srch+=($1); done
    echo "search ${srch[@]}"
    for i in ${enabled[@]}; do
        echo "op $i"
        for s in ${srch[@]}; do
            echo "srch $s"
            [[ $i == $s ]] && {
                echo "found!"
                return 0
            }
        done
    done

    return 1
}
