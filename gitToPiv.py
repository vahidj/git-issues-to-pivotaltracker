from github import Github

import requests

projId = "your_pivotaltracker_project_id" #you can extract this from pivotaltracker website
token = "your_pivotaltracker_token" #you can extract this from pivotaltracker website
myUserId = "your_pivotaltracker_user_id"

headers = {"X-TrackerToken": token}
serviceUrl = "https://www.pivotaltracker.com/services/v5/projects/"+projId+"/stories"
print serviceUrl

#payload = {"current_state":"unscheduled", "name": "test", "description":"test", "story_type":"test", "requested_by_id": 123}

#r = requests.post(serviceUrl, json=payload)

#exit()


g = Github("your_git_user_id", "your_git_password")

repo = g.get_user().get_orgs()[1].get_repo("your_git_repo_name")

print ("Number of issues to be migrated: " + str(repo.get_issues().totalCount))

for issue in repo.get_issues():
	payload = {"current_state":"unstarted", "requested_by_id": int(myUserId), "project_id":int(projId)}
	payload["name"] = issue.title
	payload["description"] = issue.body

	story_type = "feature"
	for label in issue.labels:
		if label.name == "TYPE:Bug":
			story_type = "bug"
	payload["story_type"] = story_type
	comments = []
	for comment in issue.get_comments():
		comments.append({"text":comment.body})
	payload["comments"] = comments
	r = requests.post(serviceUrl, data=payload, headers=headers)
	print(str(r))
	print str(payload)
