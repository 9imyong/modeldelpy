# scripts/gen_password.sh (Linux용)
#!/usr/bin/env bash
# Usage: ./scripts/gen_password.sh <plain_password>
if [ -z "$1" ]; then
  echo "Usage: $0 <plain_password>"
  exit 1
fi
PLAIN_PASS=$1
HASH=$(python3 - << 'EOF'
from utils.security import hash_password
print(hash_password("$PLAIN_PASS"))
EOF
)
ENV_FILE="$PWD/.env"
if grep -q '^ADMIN_PASSWORD_HASH=' "$ENV_FILE"; then
  sed -i "s|^ADMIN_PASSWORD_HASH=.*|ADMIN_PASSWORD_HASH=$HASH|" "$ENV_FILE"
else
  echo "ADMIN_PASSWORD_HASH=$HASH" >> "$ENV_FILE"
fi
echo "Updated ADMIN_PASSWORD_HASH in .env: $HASH"