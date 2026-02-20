output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}

output "lambda_security_group_id" {
  value = aws_security_group.lambda_security_group.id
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}