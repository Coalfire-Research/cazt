umask 0377

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR"

openssl req -x509 -newkey rsa:4096 -nodes -out "$SCRIPT_DIR/server.crt" -keyout "$SCRIPT_DIR/server.key" -days 3653 -subj "/CN=cazt.us-texas-9.cloud.localtest.me"
