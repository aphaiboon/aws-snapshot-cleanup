# Dev Logs

---

### Feb 20, 2026 @ 7:12 AM

Hello!

This file is used to document my whole thought process as I am tackling this snapshot cleanup task. If you would like the general overview of my thought process, please read the readme.md instead!

It has been a minute since I have utilized IaC for CI/CD processes since AI/Vibe coding has been on a rise. I have been primarily utilizing serverless architecture, since most startup/contract positions do not need a more custom process.

Most startups will have the below.

- Monorepo
- Monolithic architecture
- small team of less than 5.

Making it make sense for us to only need a staging environemnt (Which I primarily utilize, while others purely "vibe code" from their local environment), and production environment.

Other places I have been at can easily get by with just utilizing Vercel/Railway and be okay.

---

Knowing this, I will start today, with setting up my environment with AWS CLI & Terraform.

Note: I will be documenting my though processes deeply in this dev-logs folder to provide a way for you to understand how my mind works as I work through out the tasks and its list.

---

I am debating if I want to create just 1 file and keep adding onto it as my though process goes? or have a single index file, and that will reference my progress and though process, kind of like git commits? We will see as I proceed.

---

### Feb 20, 2026 @ 7:28 AM

**Setup Terraform:**

Since my other environments were company laptops. I have to setup everything on my personal space to prepare for this task. I reached an error:

```
==> Installing terraform from hashicorp/tap
Error: Your Command Line Tools (CLT) does not support macOS 26.
It is either outdated or was modified.
```

- **Cause:** most recent macos doesnt allow brew to install it.
- **Proposed solution:** download the binary directly and install.
- **Result:** Success.

```
aws-snapshot-cleanup % terraform version
Terraform v1.14.5
on darwin_arm64
```

---

**Setup AWS CLI**

Running:

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

Result:

```
aws-snapshot-cleanup % aws --version
aws-cli/2.33.26 Python/3.13.11 Darwin/25.3.0 exe/arm64
(base) aphaiboon@Mac-899 aws-snapshot-cleanup %
```
