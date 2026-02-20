# Project Plan

---

## Phase 0: Setup
- Setup Local
- Create AWS Account & Link to CLI

---

## Phase 1: Project Base & Configuration
- Create files/folders for terraform & project.
- Configure Terraform to connect to AWS account

---

## Phase 2: VPC Setup
- Create VPC
- Create & connect private subnet.
- Create a Security Group for Lambda (allow outbound to AWS APIs, no inbound needed)

---

## Phase 3: IAM Role
- Define IAM role for Lambda with least-privilege permissions.
- Only needs two things: permission to list snapshots, and permission to delete them.

---

## Phase 4: Lambda Configuration
- Create lambda function to pull ALL snapshots.
  - **Note:** Use `OwnerIds=['self']` in `describe_snapshots()` to scope results our account only.
- Check if any snapshots exist before proceeding. If none, log and exit cleanly.
- Filter snapshots older than one year.
- Attach Lambda to the VPC (subnet IDs + security group ID in Terraform).
- Delete old snapshots, while logging:
  - Deleting snapshot: [snapshot_id]
  - Log success or failure per snapshot.
  - Include basic error handling for API calls.

---

## Phase 5: Daily Scheduler
- Setup AWS EventBridge Rule to trigger the Lambda function daily.

---

## Phase 6: Implement Automated Testing
- Install and write automated testing via Moto to confirm code is working as intended.

---

## Phase 7: Deployment
- Terraform zips the Python code and deploys it to AWS as part of `terraform apply`.
- Document the full deployment process so anyone can replicate it from scratch.

---

## Phase 8: Documentation (README)
- Embed architecture diagram in README.
- Why Terraform was chosen over CloudFormation.
- How to execute the IaC to create the infrastructure (VPC, subnet, IAM role, EventBridge rule).
- How to deploy the Lambda function code.
- How to configure the Lambda to run within the VPC (subnet IDs, security group IDs).
- Assumptions made (e.g., AWS region, snapshot ownership scoped to account).
- How to monitor the Lambda's execution (CloudWatch Logs, CloudWatch Metrics).
