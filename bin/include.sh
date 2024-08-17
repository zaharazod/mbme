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

# dbsetting() {
#     # FIXME:  pg specific
#     x=$1
#     echo "
# from configparser import ConfigParser
# parts = r'$x'.split('.')

# config = ConfigParser()
# config.read('$root/config/pg_service.conf')
# for section in config.sections():


#     " | python
# }
