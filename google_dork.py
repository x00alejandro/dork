import os

class GoogleDork:
    def __init__(self, keyword):
        self.keyword = keyword
        self.GOOGLE = "https://www.google.com/search?q=site%3A"

    def is_output_file_missing_or_empty(self, file_path):
        return not (os.path.exists(file_path) and os.path.getsize(file_path) > 0)

    def generate_raw_links(self):
        google_links = []
        if self.is_output_file_missing_or_empty(f"google_dork_links_{self.keyword}_raw.txt"):
            with open(f"google_keywords.txt", "r") as keywords_file:
                with open(f"google_dork_links_{self.keyword}_raw.txt", "w") as raw_file:
                    for line in keywords_file:
                        line = line.strip()
                        line = line.replace(" ", "+")
                        modified_line = f"{self.GOOGLE}{self.keyword}+{line}\n"
                        google_links.append(modified_line)
                        raw_file.write(modified_line)
        return google_links

    def generate_verbose_links(self):
        google_links = []
        if self.is_output_file_missing_or_empty(f"google_dork_links_{self.keyword}_verbose.txt"):
            with open(f"google_keywords_verbose.txt", "r") as keywords_file:
                with open(f"google_dork_links_{self.keyword}_verbose.txt", "w") as verbose_file:
                    for line in keywords_file:
                        line = line.strip()
                        if not line:
                            verbose_file.write("\n")
                        elif line.startswith("### DORK TYPE:"):
                            verbose_file.write(f"{line}\n")
                        else:
                            line = line.replace(" ", "+")
                            modified_line = f"{self.GOOGLE}{self.keyword}+{line}\n"
                            google_links.append(modified_line)
                            verbose_file.write(modified_line)
        return google_links
