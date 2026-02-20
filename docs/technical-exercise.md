# Technical Exercise

## Scenario

You need to design and implement an AWS Lambda function that runs within a specified VPC and automatically deletes EC2 snapshots older than one year.

---

## Requirements

### 1. Infrastructure as Code (IaC)

Define the necessary AWS infrastructure using either **Terraform** or **AWS CloudFormation**. This should include:

- A VPC and at least one private subnet.
- An IAM role for the Lambda function with the correct permissions.
- *(Optional, but bonus points)*: A CloudWatch Event Rule (or EventBridge Rule) to trigger the Lambda function on a schedule (e.g., daily).

### 2. Lambda Function Code

Write the Python code for the Lambda function that:

- Connects to the AWS EC2 service.
- Retrieves a list of all EC2 snapshots in the specified region.
- Filters the snapshots to identify those older than one year (calculate the age based on the snapshot's `StartTime`).
- For each identified old snapshot, attempts to delete it.
- Logs the actions taken (e.g., `"Deleting snapshot: [snapshot_id]"`).
- Includes basic error handling for API calls.

### 3. Deployment

Describe how you would package and deploy the Lambda function (e.g., using the AWS CLI, Serverless Framework, or Terraform).

### 4. Documentation

Provide a brief README file explaining:

- The chosen IaC tool and why.
- How to execute the IaC to create the infrastructure (VPC, subnet, IAM role, CloudWatch Event Rule if included).
- How to deploy the Lambda function code.
- How to configure the Lambda function to run within the VPC (subnet IDs, security group IDs).
- Any assumptions made during the implementation (e.g., AWS region).
- How you would monitor the Lambda function's execution (e.g., CloudWatch Logs, CloudWatch Metrics).
- Create a diagram explaining the design and all implementation. It should show all infrastructure components.
