class Bit_url:
    
    def __init__(self, username,branch_name):
        self.username = username
        self.branch_name = branch_name

    def post_manager(self):
        repo_url = f"https://{self.username}@bitbucket.org/ewire_tech_team/ewire-framework.git"
        clone_command = f"git clone -b {self.branch_name} {repo_url}"
        return clone_command
 