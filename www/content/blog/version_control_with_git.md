
---
draft: false
title: Version Control with GIT
weight: 10
description: A foundational guide for data science teams using Git and GitLab to manage their programming projects.
date: 2024-01-01
lastmod: 2024-01-01
---

This document provides a practical overview for data science teams implementing Git and GitLab for software project management. It emphasizes the role of version control as a critical safeguard, enabling collaborative development through branching. The guide details essential concepts such as branching, which promotes independent development of features.
<!--more-->

Furthermore, it explains the lifecycle of a merge request, highlighting the capabilities of GitLab in facilitating code review and maintaining stable release processes. The text also outlines practical commands and integrates these tools to ensure traceability and project stability throughout the entire development process.

{{<figure src="imgs/gitlab_workflow_handbook00.png" width="800" alt="Title" >}}

*Listen to the introduction:*

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Git_Staging_Branching_and_Merge_Requests.m4a" type="audio/mp4" />
    Your browser does not support the audio element.
</audio>

*Resources:*
- [Pro Git book](https://git-scm.com/book/en/v2), a free e-book.
- [https://git-scm.com/install/] Install git on Windows, macOS, or Linux

---


<!-- ## How to Use Version Control with Git: A Practical Guide for Teams -->
{{<figure src="imgs/gitlab_workflow_handbook01.png" width="800" alt="Collaboration with Chaos" >}}



If you’re building software with a team, version control is your safety net. It keeps track of every change, prevents lost code, and enables collaboration without chaos. Git is the most widely used version control system today — it allows developers to work independently, merge their contributions, and manage releases in a structured way.

<!-- ### Understanding How Git Works -->

{{<figure src="imgs/gitlab_workflow_handbook02.png" width="800" alt="Distributed Archtitecture" >}}

At its core, Git is a distributed version control system. This means every developer has a full copy of the code repository, including its entire history. Changes are made locally before being synchronized with a central remote server (like GitLab or GitHub).

{{<figure src="imgs/gitlab_workflow_handbook03.png" width="800" alt="Three Stages of File Tracking" >}}

The basic Git workflow involves three stages:

1. **Working Directory** – Where you edit files.
2. **Staging Area (Index)** – Where you mark files you want to include in your next commit.
3. **Repository (Local Repo)** – Where your commits are stored permanently as snapshots of your project.

Once your local repository contains commits, you can **push** them to a remote Git server so your teammates can see and integrate your work.

<!-- ### What Is a Code Repository? -->
{{<figure src="imgs/gitlab_workflow_handbook04.png" width="800" alt="The Repository: Your Project's Core" >}}

A **repository (repo)** is the core concept in Git — it’s a project directory that stores your source code along with a hidden `.git` folder containing all version history and configuration data. Repositories can be either:

- **Local repositories**, stored on your own machine.
- **Remote repositories**, hosted on platforms like GitLab, where they act as the central source of truth for the team.



<!-- ### Branches vs. Forks -->

{{<figure src="imgs/gitlab_workflow_handbook05.png" width="800" alt="Branches vs Forks" >}}

Branches and forks help developers work on separate versions of code:

- **Branch** – A lightweight, parallel version of the same repository. When you create a branch (e.g., `feature-login`), you can develop and commit changes without affecting the main branch.
- **Fork** – A full copy of another repository, usually used when contributing to a project you don’t have write access to. It’s more common in open-source workflows than within small teams.

Most teams primarily use **branching** for daily collaboration.

<!-- ### Team Collaboration on GitLab -->
{{<figure src="imgs/gitlab_workflow_handbook06.png" width="800" alt="Daily Workflow" >}}

GitLab acts as your shared Git server and collaboration platform. A typical team workflow looks like this:

1. The team agrees on a shared branch — often named `develop` — as the **integration branch** or current source of truth.
2. Each developer creates a personal branch from `develop`, e.g., `feature-api-endpoint`.
3. They make changes locally, using cycles of add → commit → push to evolve their branch.
4. Once ready and tested, the developer creates a **merge request** (or “pull request”) in GitLab to incorporate their work into `develop`.
5. GitLab allows teammates to **review**, **comment on**, and **approve** merge requests.
6. If there are conflicting changes, Git signals a **merge conflict**, which must be resolved manually before merging.
7. Once merged, each developer starts a new private branch for the next feature.

This branching strategy keeps the `develop` branch clean and stable while enabling fast parallel work across the team.

<!-- ### Release Management with Dedicated Branches -->
{{<figure src="imgs/gitlab_workflow_handbook07.png" width="800" alt="The Integration: Merge Request" >}}

Teams often use multiple long-lived branches to manage different project stages:

- **`develop`** – The main working branch for new features.
- **`uat` (User Acceptance Testing)** – Created from `develop` when the team wants a stable snapshot for testing or client review.
- **`main`** – Represents the official production-ready version.

{{<figure src="imgs/gitlab_workflow_handbook08.png" width="800" alt="Release Management Strategy " >}}
A common release flow looks like this:

1. When `develop` reaches a reviewable state, it’s merged into `uat`.
2. The `uat` branch is deployed or tested externally while development continues on `develop`.
3. Once approved, `uat` merges into `main`, marking the official release version.

This approach ensures that stable and in-progress versions of your project can coexist safely.


{{<figure src="imgs/gitlab_workflow_handbook09.png" width="800" alt="The Lifecycle: Idea to Production" >}}


<!-- ### Basic Git Commands -->

{{<figure src="imgs/gitlab_workflow_handbook10.png" width="800" alt="Command Reference" >}}

Here’s a quick command-line guide for daily Git usage:

```bash
# Clone a repository (via SSH)
git clone git@git.insight.gsu.edu/yourteam/yourrepo.git

# Create and switch to a branch
git checkout -b feature-login

# Stage modified files
git add .

# Commit changes locally
git commit -m "Implement login functionality"

# Push your branch to remote
git push -u origin feature-login

# Update your local repo from the remote develop branch
git checkout develop
git pull origin develop

# After merge approval, merge changes locally (if needed)
git merge feature-login
```


<!-- ### Git in Modern Development Environments -->

{{<figure src="imgs/gitlab_workflow_handbook11.png" width="800" alt="Toolkit Integration" >}}


Most modern tools integrate Git directly:

- **VS Code** and **JupyterLab** let you view diffs, commit changes, and manage branches through intuitive interfaces.
- However, the **GitLab web interface** excels in visualizing merge requests, reviewing changes, tracking issues, and managing CI/CD pipelines. It’s where collaboration and decision-making happen.

{{<figure src="imgs/gitlab_workflow_handbook12.png" width="800" alt="Shared Language of Collaboration" >}}


Git isn’t just about code history — it’s a shared language of collaboration. From solo projects to large-scale enterprise systems, Git with GitLab provides structure, traceability, and confidence that your team’s code evolves safely and coherently.





<!-- {{<figure src="imgs/gitlab_workflow_handbook02.png" width="800" alt="Figure 3" >}} -->


<!-- {{<figure src="imgs/gitlab_workflow_handbook05.png" width="800" alt="Figure 6" >}} -->



