<div id="back-to-top"></div>


# Github Useful Commands

<details> <summary>Commands</summary>

## Deletes branch references to remote branches that do not exist
```
git remote prune origin
```

## Count the number of lines in all the files tracked by Git

```
git ls-files | xargs wc -l
```

## Count Only Specific File Types

```
git ls-files '*.js' '*.cs' | xargs wc -l
```

<div align="right">&#8673; <a href="#back-to-top" title="Table of Contents">Back to Top</a></div>

</details>

# GitHub Repository Splitting

<details>  <summary>GitHub Repository Splitting</summary>

> [!IMPORTANT]
> Install Python

## Prerequisite

```
pip install git-filter-repo
```

## Move all the files with same folder structure:

 ```
 git filter-repo --path aaa/ddd --force
 git ls-tree -r HEAD --name-only
 git remote add splited-new-repo-local-name https://github.com/Infinite-demo/Split-1.git
 git push splited-new-repo-local-name main
```

 ## Move all the files to new folder(test):

 ```
 git filter-repo --path aaa/ddd --force --path-rename aaa/ddd:test
 git ls-tree -r HEAD --name-only
 git remote add splited-new-repo-local-name https://github.com/Infinite-demo/Split-2.git
 git push splited-new-repo-local-name main
```

 ## Move all the files to Root:

 ```
 git filter-repo --subdirectory-filter aaa/ddd/ --force
 git ls-tree -r HEAD --name-only
 git remote add splited-new-repo-local-name https://github.com/Infinite-demo/Split-3.git
 git push splited-new-repo-local-name main
```

<div align="right">&#8673; <a href="#back-to-top" title="Table of Contents">Back to Top</a></div>

</details>

# Markdown Cheat Sheet

<details> <summary>GitHub Markdown Cheat Sheet</summary>

[The Ultimate Markdown Cheat Sheet](https://github.com/lifeparticle/Markdown-Cheatsheet)

[Quick Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

[Github markdown emoji](https://gist.github.com/rxaviers/7360908)

<div align="right">&#8673; <a href="#back-to-top" title="Table of Contents">Back to Top</a></div>

</details>



