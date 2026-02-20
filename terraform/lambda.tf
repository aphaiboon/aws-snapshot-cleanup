# Zip up the lambda function.
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda.zip"
}

# Wire Lambda function into the VPC with IAM role attached
resource "aws_lambda_function" "snapshot_cleanup" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.project_name}-lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "handler.handler"
  runtime          = "python3.13"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 300

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda_security_group.id]
  }
  environment {
    variables = {
      CUTOFF_DAYS = "365"
    }
  }

  tags = {
    Name = "${var.project_name}-lambda"
  }
}
