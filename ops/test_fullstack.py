#!/usr/bin/env python
import re
import subprocess
import sys
import time

import requests

TIME_LIMIT = 10 * 60  # seconds
MODULE_NAMES = {"default", "py3-web", "py3-api", "py3-tasks-io"}

# Wait up to |TIME_LIMIT| for all modules to start and webpack to build
startup_success = False
start_time = time.time()
while time.time() - start_time < TIME_LIMIT and not startup_success:
    # Check for started modules
    result = subprocess.run(
        ["vagrant", "ssh", "--", "-t", "cat /var/log/tba.log"], stdout=subprocess.PIPE
    )
    started = set(
        re.findall(r"Starting module \"(.*)\"", result.stdout.decode("utf-8"))
    )
    not_started = MODULE_NAMES.difference(started)
    if not_started:
        print(f"Not started modules: {not_started}")
        time.sleep(5)
        continue
    print(f"Started modules: {started}")

    # Check for webpack build
    result = subprocess.run(
        ["vagrant", "ssh", "--", "-t", "cat /var/log/webpack.log"],
        stdout=subprocess.PIPE,
    )
    m = re.search(
        r"webpack .* compiled successfully in .*", result.stdout.decode("utf-8")
    )
    if not m:
        print("Webpack not compiled")
        time.sleep(5)
        continue
    print(m.group(0))
    startup_success = True

if startup_success:
    # Check home page
    try:
        url = "http://localhost:8080"
        r = requests.get(url)
        if r.status_code == 200:
            if "The Blue Alliance" in r.text:
                print("Success: Home page loaded")
                sys.exit(0)
            else:
                print("Fail: 200 with unexpected content")
                sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

print("Fail: Didn't start up in time")
sys.exit(1)