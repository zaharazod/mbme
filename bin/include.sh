
export root=$(realpath "$(dirname $BASH_SOURCE)/../")
export PYTHONPATH=$root:$PYTHONPATH
export PATH=$root/bin:$PATH

setting() {
    x=$1
    echo "
from config import config
parts = r'$x'.split('.')
ctx = config.settings
while len(parts):
    part = parts.pop(0)
    if isinstance(ctx, dict):
        ctx = ctx.get(part, '')
    else:
        break
print(ctx)
    " | python
}
