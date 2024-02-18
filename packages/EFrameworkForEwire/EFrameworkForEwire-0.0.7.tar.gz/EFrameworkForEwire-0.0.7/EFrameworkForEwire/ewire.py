class Bit_url:
    
    def __init__(self, username):
        self.username = username

    def customer__onboard(self):
        repo_url = f"https://{self.username}@bitbucket.org/ewire_tech_team/ccp_customer__onboard_core.git"
        clone_command = f"git clone {repo_url}"
        return clone_command
