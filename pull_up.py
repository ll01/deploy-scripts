import subprocess
import shlex
import os


def main():
    run_command("add-apt-repository ppa:longsleep/golang-backports")
    run_command("apt-get update -y")
    install_package("golang-go")
    install_package("curl")
    install_package("git")
    run_command("curl -fsSL get.docker.com -o get-docker.sh")
    run_command("sh get-docker.sh")
    run_command('mkdir src')
    os.chdir("./src")
    run_command('git clone -b v2 "https://github.com/caddyserver/caddy.git"')
    os.chdir("./caddy/cmd/caddy/")
    run_command('go build')
    run_command("./caddy run  ")


def run_command(cmd):
    cmd = shlex.split(cmd)
    print(cmd)
    process = subprocess.Popen(
        cmd, stdin=subprocess.PIPE)
    returnCode = process.wait()
    if returnCode != 0:
        print("Error running command")
        print(process.stderr)


def install_package(package_name, install_base_command="apt-get install -y"):
    return run_command("{} {}".format(install_base_command, package_name))

if __name__ == "__main__":
    main()
