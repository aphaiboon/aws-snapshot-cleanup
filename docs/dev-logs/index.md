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

---

### Feb 20, 2026 @ 12:34 PM — Phase 3

This phase we have to setup the IAM role for the Lambda function.

Created `iam.tf` with three resources:

1. **IAM Role** — the role itself, with a trust policy that allows the Lambda function to assume it.
2. **Inline Policy** — scoped to only the two permissions the Lambda actually needs:
   - `ec2:DescribeSnapshots`
   - `ec2:DeleteSnapshot`
3. **Policy Attachment** — attached AWS managed policy `AWSLambdaVPCAccessExecutionRole`. This handles CloudWatch Logs access and VPC network interface creation so Lambda can actually run inside the VPC.

> **Note:** Ran into a small issue — typed in the wrong resource name `aws_iam_policy` instead of `aws_iam_role_policy`. These are two completely different resources. Caught it before applying. Intellisense eh? haha.

---

### Feb 20, 2026 @ 1:10 PM — Phase 4

Phase 4 is the big one — where the actual Lambda function gets built and wired into everything.

---

**`lambda/handler.py`** — the Python cleanup script.

What it does:
1. Reads `CUTOFF_DAYS` env variable (defaults to 365 if not set)
2. Connects to AWS EC2
3. Pulls snapshots owned by the account using `OwnerIds=["self"]`. If I didn't add this, it would pull other public snapshots from across AWS.
4. If no snapshots exist at all, logs it and exits cleanly.
5. Filters snapshots older than the cutoff date using `StartTime`.
6. If none are old enough, logs and exits.
7. Loops through old snapshots, attempts to delete each one, logs success or failure per snapshot.

---

**`terraform/lambda.tf`** — wires the Lambda function into the infrastructure.

- Points Terraform to the Python code and zips it automatically on `terraform apply`.
- Attaches the IAM role from Phase 3.
- Places Lambda inside the private subnet using the security group from Phase 2.
- Sets `CUTOFF_DAYS = 365` as an environment variable (can be overridden for testing).
- `timeout = 300` — gave it 5 minutes to handle large snapshot counts.

---

**A few issues I ran into:**

1. Had to fix the source path for the zip. Initially set it to `${path.module}/lambda` when it needed to be `${path.module}/../lambda`. The `../` is needed because the `terraform/` folder and the `lambda/` folder are siblings, not nested.
2. Forgot to add `hashicorp/archive` to `provider.tf` — `archive_file` requires it as a provider.
3. `boto3` wasn't installed locally so the editor was flagging the import. Installed it locally to silence the warning. It's pre-installed in the AWS Lambda runtime so it doesn't need to be bundled.

---

After running terraform commands, the Lambda took ~4 minutes to deploy because AWS had to provision the network interfaces in the subnet first.

`terraform apply` — successful. Lambda is live.

---

### Feb 20, 2026 @ 1:29 PM — Phase 5

Short phase, daily scheduler. 

Created a `scheduler.tf` with three resources. 
1. EventBridge rule = schedules the lambda to run daily at 8:00 AM UTC using cron. 
2. Event Target = schedules the lambda function. (what actually runs on the trigger)
3. Lambda Permission = gives EventBridge permission to invoke the lambda. Easy to forget, since IAM role covers what lambda can do, eventbridge still needs its own permission. 

Note: Terraform resource is still called `aws_cloudwatch_event_rule` even though aws rebranded to EventBridge.

`terraform apply` - successful. 