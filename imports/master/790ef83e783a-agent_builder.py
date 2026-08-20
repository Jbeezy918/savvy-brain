import paramiko

class BobTheBuilder:
    def __init__(self, target_ip, username="root"):
        self.target_ip = target_ip
        self.username = username
        self.ssh = None
        
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.target_ip, username=self.username)
        print("[Bob_Builder] Cryptographic root tunnel open.")

    def build_repo(self, repo_url, folder_name):
        """Clones custom integration repositories directly into Home Assistant."""
        target_path = f"/config/custom_components/{folder_name}"
        print(f"[Bob_Builder] Injecting component from: {repo_url}")
        
        # Pulls code directly via the secure shell terminal execution
        cmd = f"git clone {repo_url} {target_path} || (cd {target_path} && git pull)"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        
        out = stdout.read().decode().strip()
        if out: print(f"[System] {out}")
        print(f"[Bob_Builder] Component {folder_name} is locked and loaded.")

    def close(self):
        if self.ssh:
            self.ssh.close()
            print("[Bob_Builder] Tunnel safely closed.")

if __name__ == "__main__":
    builder = BobTheBuilder(target_ip="192.168.68.110")
    try:
        builder.connect()
        # Automate the deployment pipeline for additional custom tracking tools
        builder.build_repo("https://github.com/custom-components/alexa_media_player.git", "alexa_media_player")
    finally:
        builder.close()
