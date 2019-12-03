import json
import urllib
import subprocess
import shlex
import os

# git clone https://username:password@github.com/username/repo_name.git


def main():
    appData = json.loads("deploy_settings.json")
    if  os.path.isdir(appData.path):
        run_command("git pull")
    else:
        run_command("git clone {} {}".format(appData.registry, appData.path))
    run_command("docker-compose pull")
    run_command("docker-compose stop")
    run_command("docker-compose rm -f")
    run_command(
        "docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d")
    postNewConfig(appData.name, appData.config)
        

def run_command(cmd):
    cmd = shlex.split(cmd)
    print(cmd)
    process = subprocess.Popen(
        cmd, stdin=subprocess.PIPE)
    returnCode = process.wait()
    if returnCode != 0:
        print("Error running command")
        print(process.stderr)


def postNewConfig(name, config):
    data = urllib.parse.urlencode(config).encode()
    req = urllib.request.Request(
        "http://localhost:2019/config/{}".format(name), data=data)
    req.get_method = lambda: 'PUT'
    resp = urllib.request.urlopen(req)


if __name__ == "__main__":
    main()
