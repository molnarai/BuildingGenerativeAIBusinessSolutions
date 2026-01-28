---
draft: false
title: Mastering Secure Shell is Key
weight: 15
description: Tutorial on setting up SSH keys 
date: 2024-01-01
lastmod: 2024-01-01
---

<!-- # Write a instruction guide for SSH. 

*Prompt used for perplexity.com:*
The audience are data scientists who need to work on remote linux servers to access the remote command line interface or transfer files, use GitLab and use SSH to tunnel network connections to private database servers or other applications.
Briefly illustrate how SSH works and the concept of private and public key pairs.
Explain how this can be used to connect to remote servers without password. Among other things, SSH can be used to run commands on remote systems, it can also be used with SCP and SFTP to transfer files.
Explain that each computer, laptop or UNIX user account need to create their own private/public key pair and share the public key with the remote server.
Given examples.
Demonstrate how to use ssh-keygen, ssh-copy-id, and how to copy the public key to the remote authorized keys if ssh-copy-id is not available like on Windows.
Next explain how the ssh key pair can be used to authenticate with git servers, like GitLab and GitHub. Demonstrate how the user copy/pastes their public key into the respective profiles.
Lastly, explain how SSH tunneling works and how it can be used to connect to a private database server. Mention that many desktop clients like DBeaver support SSH tunneling.

Write the guide in a technical, neutral tone. Use step by step instruction, e.g. "You enter..."

SSH lets you open a secure command-line session or tunnel network traffic to a remote Linux server, typically without retyping passwords once you set up keys.[^1_1]

*** -->

A comprehensive guide to Secure Shell (SSH), a vital protocol for establishing encrypted connections over networks. It details the mechanics of key-based authentication, explaining how a private and public key pair allows for secure access without traditional passwords.
<!--more -->
Practical instructions are included for generating keys, installing them on remote servers, and integrating them with platforms like GitHub and GitLab. Beyond basic logins, the source describes how to perform remote command execution and secure file transfers using SCP and SFTP. Finally, it highlights advanced workflows like SSH tunneling, which enables data scientists to access private databases securely through local port forwarding.

{{<figure src="imgs/Mastering_SSH_for_Data_Science_00.png" width="800" alt="Figure 1" >}}

*Listen to the NotebookLM intro before you start.*

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Passwordless_Login_and_Tunneling_With_SSH.m4a" type="audio/mp4" />
    Your browser does not support the audio element.
</audio>

*Watch these videos to see the use of SSH keys in action.*

<!-- <div style="margin: 20px 0;">
    <img src="https://img.youtube.com/vi/RfolgB-rVe8/mqdefault.jpg" 
         alt="SSH Tutorial Video" 
         style="width: 240px; cursor: pointer; border: 2px solid #ccc; border-radius: 4px;"
         onclick="openVideoModal('RfolgB-rVe8')" />
</div> -->

<!-- <div id="videoModal" style="display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8);" onclick="closeVideoModal()">
    <div style="position: relative; margin: 5% auto; width: 80%; max-width: 900px;">
        <span style="position: absolute; top: -40px; right: 0; color: white; font-size: 35px; font-weight: bold; cursor: pointer;" onclick="closeVideoModal()">&times;</span>
        <div id="videoContainer"></div>
    </div>
</div>
<div style="margin: 20px 0;">
    <img src="https://img.youtube.com/vi/wBQxOveSFO8/mqdefault.jpg" 
         alt="SSH Additional Tutorial" 
         style="width: 240px; cursor: pointer; border: 2px solid #ccc; border-radius: 4px;"
         onclick="openVideoModal('wBQxOveSFO8')" />
</div> -->

<div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
    <img src="https://img.youtube.com/vi/RfolgB-rVe8/mqdefault.jpg" 
         alt="SSH Tutorial Video" 
         style="width: 240px; cursor: pointer; border: 2px solid #ccc; border-radius: 4px;"
         onclick="openVideoModal('RfolgB-rVe8')" />
    <img src="https://img.youtube.com/vi/wBQxOveSFO8/mqdefault.jpg" 
         alt="SSH Additional Tutorial" 
         style="width: 240px; cursor: pointer; border: 2px solid #ccc; border-radius: 4px;"
         onclick="openVideoModal('wBQxOveSFO8')" />
</div>

<div id="videoModal" style="display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8);" onclick="closeVideoModal()">
    <div style="position: relative; margin: 5% auto; width: 80%; max-width: 900px;">
        <span style="position: absolute; top: -40px; right: 0; color: white; font-size: 35px; font-weight: bold; cursor: pointer;" onclick="closeVideoModal()">&times;</span>
        <div id="videoContainer"></div>
    </div>
</div>

<script>
function openVideoModal(videoId) {
    document.getElementById('videoModal').style.display = 'block';
    document.getElementById('videoContainer').innerHTML = 
        '<iframe width="100%" height="500" src="https://www.youtube.com/embed/' + videoId + '?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
}

function closeVideoModal() {
    document.getElementById('videoModal').style.display = 'none';
    document.getElementById('videoContainer').innerHTML = '';
}
</script>

<!-- https://youtu.be/RfolgB-rVe8 -->

***


<!-- ## 1. What SSH is and how it works -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_01.png" width="800" alt="What is SSH" >}}
SSH (Secure Shell) is a protocol for encrypted remote login and command execution over an insecure network.[^1_1]

When you connect with SSH:

- Your client and the server negotiate encryption and establish a shared session key, so all traffic is encrypted in transit.[^1_2]
- The server proves its identity with its **host key**, which your client stores and checks on later connections.[^1_3]
- You authenticate as a user, either with a password or with an SSH key pair.[^1_1]

For data scientists, SSH is the standard way to:

- Get a remote shell on Linux servers.
- Run commands and scripts remotely (e.g., `ssh server 'python script.py'`).
- Transfer files with SCP or SFTP.
- Authenticate to Git servers (GitLab, GitHub).
- Create tunnels to internal resources like databases.


<!-- ## 2. SSH key pairs: public vs private -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_02.png" width="800" alt="Key Pairs" >}}

An SSH key pair is two mathematically related keys: a **private** key and a **public** key.[^1_4][^1_1]

- The **private** key stays on your laptop or workstation; it must be kept secret and protected by file permissions and optionally a passphrase.[^1_4][^1_1]
- The **public** key is safe to share and is copied to each remote account or service you want to access.[^1_4][^1_1]

In key-based authentication:

1. You start an SSH connection to `user@server`.
2. The server checks whether your public key is listed in that account’s `~/.ssh/authorized_keys` file.[^1_5]
3. If it is, the server sends an encrypted challenge that only someone with the matching private key can answer correctly.[^1_2]
4. Your client proves possession of the private key, and the server grants access without asking for the account password.[^1_5][^1_2]

Each **user account on each physical computer** (your laptop, a VM, etc.) needs its own key pair and must share its public key with the remote systems it will access.[^1_5][^1_4]

You typically do this once per machine or per security context.

<!-- ## Generating an SSH key pair with ssh-keygen -->

<!-- ### Step 1: Generate a key pair -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_03.png" width="800" alt="Step 1: Generating Key" >}}

On Linux, macOS, or Git Bash/WSL on Windows:

1. You open a terminal.
2. You enter:

```bash
ssh-keygen -t ed25519 -C "your.name@yourorg.edu"
```

If `ed25519` is not supported, use `-t rsa -b 4096` instead.[^1_6]
3. When prompted for a file, you press Enter to accept the default `~/.ssh/id_ed25519` (or `id_rsa`).[^1_6]
4. When prompted for a passphrase, you either:
    - Enter a passphrase (recommended for laptops), or
    - Press Enter for no passphrase (less secure but can be convenient for automation).[^1_6]

This creates:

- Private key: `~/.ssh/id_ed25519`
- Public key: `~/.ssh/id_ed25519.pub`

Depending on you system and which encryption method you choose, the names may differ. However, they usually follow the format `id#####` for the private, and `id#####.pub` for the public key. If you choose against the default name and pick your own, you may have to specify the key with certain commands.

You can view your public key with:

```bash
cat ~/.ssh/id_ed25519.pub
```

You will copy-paste or upload this `.pub` file to servers and Git services.


<!-- ## 4. Installing your public key on a remote server -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_04.png" width="800" alt="Step 2: Installling Key" >}}

The goal is to add your public key to `~/.ssh/authorized_keys` on the remote account so you can log in without a password.[^1_7][^1_5]

<!-- ### 4.1 Using ssh-copy-id (Linux/macOS, some Windows environments) -->

If `ssh-copy-id` is available (all Linux/macOS, some Windows environments):

1. You ensure you can log in with your password at least once (this is needed to install the key).
2. You enter:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub youruserid@remote.host.edu
```

This logs into the server, creates `~/.ssh` if needed, and appends your public key to `~/.ssh/authorized_keys` with correct permissions.[^1_8][^1_7]

After that:

```bash
ssh youruserid@remote.host.edu
```

should log you in without asking for the account password (it may ask for your key passphrase instead).

<!-- ### 4.2 Manual installation (no ssh-copy-id, e.g., Windows) -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_05.png" width="800" alt="Step 2: Alternative" >}}

If `ssh-copy-id` is not available, you manually append your public key to `authorized_keys`:

1. On your local machine, you display and copy your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

2. You SSH into the remote server with your password:

```bash
ssh youruserid@remote.host.edu
```

3. On the remote server, you ensure `.ssh` exists with correct permissions:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

4. You open (or create) `authorized_keys` and paste your public key at the end. Examples:
    - Using `nano`:

```bash
nano ~/.ssh/authorized_keys
```

    - Or append via echo (if you have the key in a file on the remote):

```bash
cat id_ed25519.pub >> ~/.ssh/authorized_keys
```

5. You set permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```


From now on, you can log in with:

```bash
ssh youruserid@remote.host.edu
```



<!-- ## 5. Using SSH for remote commands and file transfer -->
<!-- ### 5.1 Remote shell and command execution -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_06.png" width="800" alt="Remote Shell Execution" >}}

- Interactive shell:

```bash
ssh youruserid@remote.host.edu
```

- Run a single command:

```bash
ssh youruserid@remote.host.edu 'python train_model.py --epochs 10'
```


This is handy for running jobs or quick checks from your laptop.

<!-- ### 5.2 SCP: copying files -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_07.png" width="800" alt="Moving Files" >}}

SCP (Secure Copy) transfers files over SSH.[^1_1]

- Copy local file to remote directory:

```bash
scp results.csv youruserid@remote.host.edu:~/experiments/
```

- Copy remote file to local:

```bash
scp youruserid@remote.host.edu:~/experiments/results.csv .
```

- Copy directories recursively:

```bash
scp -r data/ youruserid@remote.host.edu:~/datasets/
```

<!-- ### 5.3 SFTP: interactive file transfer -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_08.png" width="800" alt="SFTP" >}}

SFTP gives an interactive file-transfer session over SSH.

1. You enter:

```bash
sftp youruserid@remote.host.edu
```

2. You use commands like `ls`, `cd`, `put`, `get`, `mkdir`, `rm` inside the SFTP prompt.

For example:

```bash
sftp> put local_file.csv
sftp> get remote_file.parquet
```




<!-- ## 6. Using SSH keys with GitLab and GitHub -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_09.png" width="800" alt="GitLab and GitHub" >}}
Git over SSH uses the same key pair mechanism for authenticating Git operations (clone, pull, push).[^1_9]

#### Prepare your key

You first generate a key as in section 3 and ensure your public key exists:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire single-line key (starting with `ssh-ed25519` or `ssh-rsa`).

#### Add key to GitLab

1. You log into GitLab via browser.
2. You navigate to your **Profile** → **Preferences** → **SSH Keys** (or similar; exact UI can vary).[^1_9]
3. You paste the contents of `id_ed25519.pub` into the key text box.
4. You optionally give it a title (e.g., “Laptop-2026”).
5. You click **Add key**.

You can now clone via SSH:

```bash
git clone git@gitlab.com:group/project.git
```

Git uses `~/.ssh/id_ed25519` to authenticate.

#### Add key to GitHub

1. You log into GitHub in a browser.
2. You go to **Settings** → **SSH and GPG keys**.[^1_9]
3. You click **New SSH key**.
4. You paste your public key and give it a descriptive title.
5. You save.

You can now use SSH URLs:

```bash
git clone git@github.com:org/repo.git
```

Again, Git uses the same SSH key in `~/.ssh`.

<!-- ## 7. SSH configuration for multiple servers (optional but useful) -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_10.png" width="800" alt="SSH Config File" >}}

For data scientists using many clusters or Git remotes, `~/.ssh/config` simplifies commands.

Example:

```bash
Host lab-cluster
    HostName remote.host.edu
    User youruserid
    IdentityFile ~/.ssh/id_ed25519

Host gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

Then you can run:

```bash
ssh lab-cluster
git clone git@gitlab.com:group/project.git
```

without repeatedly specifying usernames or key paths.

<!-- ## 8. SSH tunneling to private database servers -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_11.png" width="800" alt="SSH Port Tunneling" >}}

SSH tunneling (port forwarding) lets you securely reach internal services (like a PostgreSQL or MySQL server on a private network) as if they were running on your local machine.[^1_10][^1_1]

#### Concept

- The database server is reachable from the SSH host (e.g., on `localhost:5432` from the SSH server’s perspective).
- You create an SSH tunnel that forwards a local port on your laptop (e.g., `localhost:15432`) through the SSH connection to the remote database port.[^1_11][^1_10]
- Your desktop client (psql, DBeaver, Python, etc.) connects to `localhost:15432`, and the traffic is transparently sent over SSH to the remote DB.[^1_10][^1_11]


#### Command-line example: local port forward

You enter:

```bash
ssh -L 15432:localhost:5432 youruserid@remote.host.edu
```

- `15432` is the local port on your laptop.
- `localhost:5432` is the database host and port from the SSH server’s point of view.

While this SSH session is open, you can connect locally:

```bash
psql -h localhost -p 15432 -U dbuser -d mydb
```

All traffic goes through the encrypted SSH tunnel.

<!-- ### 8.3 Using SSH tunneling in DBeaver -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_12.png" width="800" alt="Using SSH tunneling in DBeaver" >}}

DBeaver and similar GUIs have built-in SSH tunneling.[^1_12][^1_11][^1_10]

A typical configuration is:

1. You create a **New Database Connection** for your DB type (PostgreSQL, MySQL, etc.).[^1_10]
2. In the main connection settings, you set:
    - Host: `localhost`
    - Port: the DB default (e.g., 5432 for PostgreSQL or 3306 for MySQL)
    - DB user and password.
3. You open the **SSH** or **SSH Tunnel** tab.
4. You enable **Use SSH Tunnel**.
5. You set:
    - SSH Host/IP: the SSH server (e.g., `remote.host.edu`)
    - SSH Port: usually `22`
    - SSH User: your SSH username
    - Authentication Method: **Public Key**
    - Private Key: path to your private key file (e.g., `~/.ssh/id_ed25519`) and passphrase if set.[^1_11][^1_12]
6. You click **Test tunnel configuration** (or similar) to verify the tunnel.[^1_12]
7. You save and connect. DBeaver now automatically creates the SSH tunnel each time and routes DB traffic through it.[^1_11][^1_12][^1_10]

Many other desktop tools (e.g., DataGrip, PgAdmin in some setups) support a similar SSH tunnel configuration.

<!-- ## 9. Practical workflow summary for data scientists -->
{{<figure src="imgs/Mastering_SSH_for_Data_Science_13.png" width="800" alt="SSH Workflow" >}}

A typical end-to-end workflow looks like:

1. You generate an SSH key pair once on your laptop with `ssh-keygen`.
2. You install your public key on:
    - Remote Linux accounts (using `ssh-copy-id` or manual `authorized_keys` setup).
    - GitLab/GitHub profiles (for Git over SSH).
3. You use:
    - `ssh` to get shells and run commands.
    - `scp`/`sftp` to move datasets, logs, and model artifacts.
    - SSH tunnels (CLI or via DBeaver) to access private databases.



Once keys are in place, almost all of this works without re-entering passwords, which is especially useful for repetitive data science tasks and automation.[^1_7][^1_9][^1_5]
<span style="display:none">[^1_13][^1_14][^1_15]</span>

{{<figure src="imgs/Mastering_SSH_for_Data_Science_14.png" width="800" alt="Automation" >}}

<div align="center">⁂</div>

[^1_1]: https://www.ssh.com/academy/ssh-keys

[^1_2]: https://blog.invgate.com/what-are-ssh-keys

[^1_3]: https://winscp.net/eng/docs/ssh_keys

[^1_4]: https://www.sectigo.com/blog/what-is-an-ssh-key

[^1_5]: https://statistics.berkeley.edu/computing/ssh-keys

[^1_6]: https://www.ssh.com/academy/ssh/keygen

[^1_7]: https://www.ssh.com/academy/ssh/copy-id

[^1_8]: https://man7.org/linux/man-pages/man1/ssh-copy-id.1.html

[^1_9]: https://www.atlassian.com/git/tutorials/git-ssh

[^1_10]: https://stackoverflow.com/questions/65481470/connect-to-remote-db-with-ssh-tunneling-in-dbeaver

[^1_11]: https://www.r-bloggers.com/2018/06/connect-mysql-database-with-dbeaver-through-ssh/

[^1_12]: https://devimalplanet.com/how-to-dbeaver-remote-database-ssh/

[^1_13]: https://www.reddit.com/r/sysadmin/comments/i3on7q/can_someone_explain_how_ssh_key_authentication/

[^1_14]: https://www.youtube.com/watch?v=RfolgB-rVe8

[^1_15]: https://www.youtube.com/watch?v=L2QM9qQ6JDg















<!-- {{<figure src="imgs/Mastering_SSH_for_Data_Science_02.png" width="800" alt="Key Pairs" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_03.png" width="800" alt="Step 1: Generating Key" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_04.png" width="800" alt="Step 2: Installling Key" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_05.png" width="800" alt="Step 2: Alternative" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_06.png" width="800" alt="Remote Shell Execution" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_07.png" width="800" alt="Moving Files" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_08.png" width="800" alt="Figure 9" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_09.png" width="800" alt="Figure 10" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_10.png" width="800" alt="Figure 11" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_11.png" width="800" alt="Figure 12" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_12.png" width="800" alt="Figure 13" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_13.png" width="800" alt="Figure 14" >}}
{{<figure src="imgs/Mastering_SSH_for_Data_Science_14.png" width="800" alt="Figure 15" >}} -->