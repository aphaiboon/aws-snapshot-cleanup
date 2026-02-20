resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

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