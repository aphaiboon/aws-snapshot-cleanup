# Dev Logs

---

### Feb 20, 2026 @ 7:12 AM — Intro

Hello!

This file is used to document my whole thought process as I am tackling this snapshot cleanup task. If you would like the general overview of my thought process, please read the readme.md instead!

It has been a minute since I have utilized IaC for CI/CD processes since AI/Vibe coding has been on a rise. I have been primarily utilizing serverless architecture, since most startup/contract positions do not need a more custom process.

Most startups will have the below.

- Monorepo
- Monolithic architecture
- small team of less than 5.

Making it make sense for us to only need a staging environment (Which I primarily utilize, while others purely "vibe code" from their local environment), and production environment.

Other places I have been at can easily get by with just utilizing Vercel/Railway and be okay.

---

Knowing this, I will start today, with setting up my environment with AWS CLI & Terraform.

> Note: I will be documenting my thought processes deeply in this dev-logs folder to provide a way for you to understand how my mind works as I work throughout the tasks and its list.

I am debating if I want to create just 1 file and keep adding onto it as my thought process goes? or have a single index file, and that will reference my progress and thought process, kind of like git commits? We will see as I proceed.

---

### Feb 20, 2026 @ 7:28 AM — Local Setup

#### Setup Terraform

Since my other environments were company laptops. I have to setup everything on my personal space to prepare for this task. I reached an error:

```
==> Installing terraform from hashicorp/tap
Error: Your Command Line Tools (CLT) does not support macOS 26.
It is either outdated or was modified.
```

- **Cause:** most recent macos doesn't allow brew to install it.
- **Proposed solution:** download the binary directly and install.
- **Result:** Success.

```
aws-snapshot-cleanup % terraform version
Terraform v1.14.5
on darwin_arm64
```

#### Setup AWS CLI

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

---

### Feb 20, 2026 @ 8:15 AM — Brainstorming & Phases

As I am reading the technical exercise document, I think I'll have to break this into phases.

I am also thinking, since I am a visual person, I should create my diagrams now, so I can visually see my phases, and setup.

---

**Phase 0: Setup**
- Setup Local ✅
- Create AWS Account & Link to CLI (so I can actually test & confirm my code)

**Phase 1: Project Base & Configuration**
- Create files/folders for terraform & project.
- Configure Terraform to connect to AWS account

**Phase 2: VPC Setup**
- Create VPC
- Create & connect private subnet.

~~**Phase 3: EC2 & Snapshot Setup**~~
~~- Setup EC2 Instance in Terraform~~
~~- Setup automatic EC2 snapshot backups in terraform~~

> **Correction:** After re-reading the exercise, I was overcomplicating this. I don't need to create EC2 instances or set up snapshot backups — that infrastructure already exists. The Lambda's only job is to query whatever snapshots are already there and clean up the old ones. Removed this phase.

**Phase 3: IAM Role**
- Define IAM role for Lambda with least-privilege permissions.
- Only needs two things: permission to list snapshots, and permission to delete them.

**Phase 4: Lambda Configuration**
- Create lambda function to pull ALL snapshots.
- Before doing anything — check if there are even any snapshots to work with. If there are none, log it and exit cleanly. No reason to proceed if there's nothing there.
- Create a filter to select backups older than one year.
- Delete those snapshots, while logging:
  - Deleting snapshot: [snapshot_id]
  - Logging success or fail, retries. etc.
  - Include basic error handling for API calls.

**Phase 5: Daily Scheduler**
- Setup AWS CloudWatch Event Rule to trigger the Lambda function daily.

**Phase 6: Implement Automated Testing**
- Install and write automated testing via Moto to confirm code is working as intended.

---

> **Note:** Phase 6 was added after correction above. Ideally I wanted to setup an AWS account to make sure my code actually functions and works as intended. Without additional steps, I think automated testing will be able to at least satisfy our needs.
>
> **Note 2:** I still may create an AWS account to confirm everything works as intended. Something irks me about not being able to be 100% certain my code works as intended in a production environment.

---

### Feb 20, 2026 @ 8:15 AM — Architecture Diagrams

Created and attached diagrams.

#### Architecture Overview

![Architecture Diagram](./diagrams/architecture.drawio.png)

#### Lambda Flow

![Lambda Flow Diagram](./diagrams/lambda-flow.drawio.png)

---

### Feb 20, 2026 @ 10:52 AM — Plan Updates

Rereading the technical exercise document, I realized I am missing 4 things.

1. Security group for the lambda.
2. Attaching lambda to the VPC.
3. Deployment
4. Documentation

I have moved the plan into a designated plan.md, and also updated the plan to correctly satisfy needs.

---

### Feb 20, 2026 @ 10:52 AM — Phase 1

This phase is to setup all the scaffolding for terraform. I have written the basic code, and made a variables.tf file to be able to replace and utilize variables instead of hardcoding it.

I have chosen the default zone to be us-east-1 — it is the AWS default & this is where AWS releases new services first. If we would like to change it, we can change it via the variables.tf file.

I renamed `main.tf` → `vpc.tf` to keep things organized, and left `outputs.tf` empty for the next phases.

Ran `terraform plan` — success. Moving on.

> **Note:** Ran into a git issue — accidentally committed the terraform provider binary cache (648MB). Had to remove it from git history entirely using `git filter-repo`. The `.gitignore` is now correctly set to prevent this going forward.

---

### Feb 20, 2026 @ 12:22 PM — Phase 2

Moving on to this phase, I setup the VPC and decided to rename `main` → `vpc.tf`. So its much easier to manage and scan for whatever the user needs. (myself included.)

Running `terraform plan` errored because I didn't have an AWS account configured. Attached an account — here's what I did:

1. Created a personal AWS account
2. IAM → Create User (`snapshot-cleanup-admin`)
3. Attached permission policies:
   - `AmazonVPCFullAccess`
   - `AWSLambda_FullAccess`
   - `IAMFullAccess`
   - `CloudWatchEventsFullAccess`
   - `AmazonEC2FullAccess`
4. Went into the new user's security credentials tab
5. Created an access key for CLI access
6. Attached keys to CLI via `aws configure`

> **Note:** Deliberately avoided using the root account for credentials. Created a dedicated IAM user with only the permissions needed for this project. Same least-privilege thinking I'm applying to the Lambda's IAM role.

Ran `terraform plan` — successful plan (3 resources to add).

Ran `terraform apply` — everything successful.

```
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:
lambda_security_group_id = "sg-0a315fbd3f703feef"
private_subnet_id        = "subnet-0af15bbe44f41311f"
vpc_id                   = "vpc-0e1820dc11bffe1a0"
```
