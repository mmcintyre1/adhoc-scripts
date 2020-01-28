""" A pygithub script that takes an access token (generated from github) and a repository name, 
and traverses the repo for csv files, and gets the file path and last modified date (last commit
date).  The resulting list could be used for whatever purpose, and the csv check can be modified. """

from github import Github

ACCESS_TOKEN = ""
REPO_NAME = ""

def get_latest_commit_date(repo, path):
    commits = repo.get_commits(path=path)
    # results are ordered, so the first item is the last commit
    # you can also return other attributes here, like commiter name, etc.
    return commits[0].commit.author.date

def get_files(repo):
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.name.endswith('.csv'):
                yield file_content

def main():
    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(REPO_NAME)
    results = []
    for file in get_files(repo):
        latest_commit = get_latest_commit_date(repo, file.path)
        # you can add other attributes if needed
        results.append([file.path, latest_commit])
    
    # do whatever with results

if __name__ == '__main__':
    main()
