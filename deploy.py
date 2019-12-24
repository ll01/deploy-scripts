import json
import urllib
import urllib.parse
import urllib.request
import subprocess
import shlex
import os

# git clone https://username:password@github.com/username/repo_name.git


def main():
    with open("deploy_settings.json", "r") as settings_file:
        appData = json.loads(settings_file.read())
        print("getting code ...")
        if  os.path.isdir(appData["path"]):
            run_command("git pull")
        else:
            run_command("git clone {} {}".format(appData["registry"], appData["path"]))
            print("composing ...")
            run_command("docker-compose pull")
            run_command("docker-compose stop")
            run_command("docker-compose rm -f")
            run_command(
                "docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d")
            postNewConfig(appData["name"], appData["config"])
        

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
    print(name)
    data = json.dumps(config).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:2019/config/apps/http/servers/{}".format(name),
         data=data, method="PUT")
    req.headers["Content-Type"] = "application/json"
    try:
        resp = urllib.request.urlopen(req)
        print( resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
  


if __name__ == "__main__":
    main()
