def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result

def install():
    run_command(cmd="cat <<EOF >> /etc/apt/sources.list.d/openmediavault.list\
deb https://packages.openmediavault.org/public usul main\
# deb https://downloads.sourceforge.net/project/openmediavault/packages usul main\
## Uncomment the following line to add software from the proposed repository.\
# deb https://packages.openmediavault.org/public usul-proposed main\
# deb https://downloads.sourceforge.net/project/openmediavault/packages usul-proposed main\
## This software is not part of OpenMediaVault, but is offered by third-party\
## developers as a service to OpenMediaVault users.\
# deb https://packages.openmediavault.org/public usul partner\
# deb https://downloads.sourceforge.net/project/openmediavault/packages usul partner\
EOF")

    run_command("sudo ./Nas-build")
if __name__ =="__main__":
    install()