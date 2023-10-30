import sys
import subprocess
from github_dork import GitHubDork
from google_dork import GoogleDork

def help():
    print("""
    -r or --raw      make GitHub dork links in raw format
    -v or --verbose  make GitHub dork links - commented version
    -g or --google   perform Google dorking
    -h or --help     display this help message
    keyword          the keyword to be used in generating the URLs
    """)

def check_and_install_requirements():
    try:
        with open("requirements.txt", "r") as requirements_file:
            required_libraries = requirements_file.read().splitlines()

        missing_libraries = []

        for library in required_libraries:
            try:
                __import__(library)
            except ImportError:
                missing_libraries.append(library)

        if missing_libraries:
            print("The following required libraries are missing:")
            for library in missing_libraries:
                print(library)
            print("Installing missing libraries...")
            for library in missing_libraries:
                subprocess.check_call(["pip", "install", library])
            print("Installation completed.")
        else:
            print("All required libraries are already installed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # check_and_install_requirements()

    github_raw_flag = False
    github_verbose_flag = False
    google_flag = False
    all_flag = False
    param = ""

    for arg in sys.argv[1:]:
        if arg in ["-r", "--raw"]:
            github_raw_flag = True
        elif arg in ["-v", "--verbose"]:
            github_verbose_flag = True
        elif arg in ["-g", "--google"]:
            google_flag = True
        else:
            param = arg

    if not param:
        print("Error: missing keyword")
        help()
        sys.exit(1)

    if not (github_raw_flag or github_verbose_flag or google_flag):
        all_flag = True

    if all_flag:
        github_raw_flag = True
        github_verbose_flag = True
        google_flag = True

    if github_raw_flag or github_verbose_flag:
        github_dork = GitHubDork(param)
        if github_raw_flag:
            github_dork.generate_raw_links()
        if github_verbose_flag:
            github_dork.generate_verbose_links()

    if google_flag:
        google_dork = GoogleDork(param)
        google_dork.generate_raw_links()

if __name__ == "__main__":
    main()
