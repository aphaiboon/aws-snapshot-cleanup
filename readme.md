# AWS Snapshot Cleanup

A Lambda function that automatically deletes EC2 snapshots older than one year. Runs daily on a schedule, lives inside a private VPC, and fully defined with Terraform.

If you want to see my full thought process as I built this, check the [dev logs](docs/dev-logs/index.md).

---

## Architecture

![Architecture Diagram](docs/dev-logs/diagrams/architecture.drawio.png)

![Lambda Flow](docs/dev-logs/diagrams/lambda-flow.drawio.png)

---

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.0
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) configured with an IAM user that has:
  - `AmazonVPCFullAccess`
  - `AWSLambda_FullAccess`
  - `IAMFullAccess`
  - `CloudWatchEventsFullAccess`
  - `AmazonEC2FullAccess`

> Don't use your root account. Create a dedicated IAM user, generate access keys, and run `aws configure`.

---

## Deploy

```bash
cd terraform
terraform init
terraform apply
```

Terraform handles everything — zipping and uploading the Lambda code included. To redeploy after code changes, just run `terraform apply` again.

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `aws_region` | `us-east-1` | AWS region to deploy into |
| `project_name` | `snapshot-cleanup` | Prefix applied to all resource names |
| `CUTOFF_DAYS` | `365` | Snapshots older than this many days get deleted |

`aws_region` and `project_name` are set in `terraform/variables.tf`. `CUTOFF_DAYS` is a Lambda environment variable configured in `terraform/lambda.tf`.

---

## Monitoring

Logs are written to CloudWatch automatically:

```
/aws/lambda/snapshot-cleanup-lambda
```

```bash
aws logs tail /aws/lambda/snapshot-cleanup-lambda --follow
```

---

## Tests

```bash
pip install 'moto[ec2]' pytest
pytest tests/ -v
```

---

## Teardown

```bash
cd terraform
terraform destroy
```
