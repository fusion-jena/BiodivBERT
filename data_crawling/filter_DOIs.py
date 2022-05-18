from os.path import realpath, join, exists
from os import listdir, makedirs

if __name__ == '__main__':
    targets = ['Springer']
    data_src_path = join(realpath('.'), 'Data')
    DOIs_path = join(data_src_path, 'DOIs')

    repos = targets
    for repo in repos:
        try:
            files = listdir(join(data_src_path, repo))
            repo_dois = []
            for filename in files:
                file_dois = []
                with open(join(data_src_path, repo, filename), 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.read().splitlines()
                    for l in lines:
                        file_dois.append(l.split('|')[0])
                    repo_dois.extend(file_dois)
            unique_repo_dois = list(set(repo_dois))

            # write it in separate files
            if not exists(DOIs_path):
                makedirs(DOIs_path)
            with open(join(DOIs_path, repo + '_unique_DOIs.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                file.write('\n'.join(unique_repo_dois))

            print(repo)
            print(len(repo_dois))
            print(len(unique_repo_dois))
        except NotADirectoryError:
            continue
        print("------------------------------")

