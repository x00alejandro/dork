class GitHubDork:
    def __init__(self, keyword):
        self.keyword = keyword

    def generate_raw_links(self):
        github_links = []
        with open(f"{self.keyword}_raw.txt", "w") as raw_file:
            with open("github_keywords.txt", "r") as keywords_file:
                for line in keywords_file:
                    modified_line = f"https://github.com/search?q=%22{self.keyword}%22+{line}&type=Code"
                    github_links.append(modified_line)
                    raw_file.write(f"{modified_line}\n")
        return github_links

    def generate_verbose_links(self):
        github_links = []
        with open(f"{self.keyword}_verbose.txt", "w") as verbose_file:
            with open("github_keywords.txt", "r") as keywords_file:
                for line in keywords_file:
                    if line.strip():
                        verbose_file.write(f"##### {line} #####\n")
                        modified_line = f"https://github.com/search?q=%22{self.keyword}%22+{line}&type=Code"
                        github_links.append(modified_line)
                        verbose_file.write(f"{modified_line}\n\n")
        return github_links
