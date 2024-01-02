setting() {
    x=$1
    echo "
from config import config
print(config.settings.get('$x',''))
    " | python
}
