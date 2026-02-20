resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  tags = {
    Name = "${var.project_name}-private-subnet"
  }
}

resource "aws_security_group" "lambda_security_group" {
  name        = "${var.project_name}-lambda-security-group"
  description = "Security group for snapshot cleanup lambda"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    self        = true
    description = "Allow HTTPS from Lambda to VPC endpoint"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow outbound traffic to AWS APIs"
  }
  tags = {
    Name = "${var.project_name}-lambda-security-group"
  }
}

# Private route to the EC2 API — required since Lambda runs in a private subnet with no internet access.
resource "aws_vpc_endpoint" "ec2" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.ec2"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [aws_subnet.private.id]
  security_group_ids  = [aws_security_group.lambda_security_group.id]
  private_dns_enabled = true

  tags = {
    Name = "${var.project_name}-ec2-endpoint"
  }
}