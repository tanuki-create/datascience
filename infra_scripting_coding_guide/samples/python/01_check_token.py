#!/usr/bin/env python3
import os
import sys

token = os.environ.get("OPSCTL_API_TOKEN")
if not token:
    print("OPSCTL_API_TOKEN is required", file=sys.stderr)
    sys.exit(1)

print("token is set", file=sys.stderr)
print(len(token))
