from collections import defaultdict
from datetime import timedelta
import matplotlib.pyplot as plt
from github import Github

# using an access token
from github.Commit import Commit
from github.Repository import Repository

# First create a Github instance:
g = Github()

repo: Repository = g.get_repo("tiangolo/fastapi")
# repo: Repository = g.get_repo("facebook/react")

# getting the date which is 31 days before last commit date
commits = repo.get_commits()
last_commit: Commit = commits[0]
month_behind_commit_date = last_commit.commit.committer.date.date() - timedelta(31)

# counting each authors commit for each date
authors = defaultdict(dict)
for commit in commits:
    author = commit.commit.author.name
    date = commit.commit.committer.date.date()
    if date <= month_behind_commit_date:
        break
    if author in ('github-actions[bot]', 'github-actions'):
        continue
    # print(author, date)

    if author in authors:
        if date in authors[author]:
            authors[author][date] += 1
        else:
            authors[author][date] = 1
    else:
        authors[author][date] = 1

# for author, dates in authors.items():
#     print(author, ":", dates)

# filling dates list with whole month dates for plotting purposes
dates = []
while month_behind_commit_date <= last_commit.commit.committer.date.date():
    dates.append(month_behind_commit_date)
    month_behind_commit_date += timedelta(1)

# filling another authors dict for plotting purposes
filtered_authors = defaultdict(dict)
for author, dates_commit_count in authors.items():
    for date in dates:
        if date in dates_commit_count:
            filtered_authors[author][date] = dates_commit_count[date]
        else:
            filtered_authors[author][date] = 0

# Plotting the collected data
plot_data = defaultdict(list)
for author, dates_commit_count in filtered_authors.items():
    for _, commit_count in dates_commit_count.items():
        plot_data[author].append(commit_count)

plt.style.use('seaborn')

for author, ccounts in plot_data.items():
    plt.plot(dates, ccounts, label=author)

plt.gcf().autofmt_xdate()

plt.legend(ncol=3)
plt.title('Number of commits for the last month')
plt.xlabel("Dates")
plt.ylabel("# of commits")

plt.tight_layout()

plt.show()
