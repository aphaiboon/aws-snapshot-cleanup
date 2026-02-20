# EventBridge Rule to trigger the Lambda function daily.
resource "aws_cloudwatch_event_rule" "daily_snapshot_cleanup" {
  name                = "${var.project_name}-daily-scheduler"
  description         = "Triggers the snapshot cleanup Lambda Daily"
  schedule_expression = "cron(0 8 * * ? *)" # Runs at 8:00 AM UTC every day. Note: we can change this to whatever time we want.
  tags = {
    Name = "${var.project_name}-daily-scheduler"
  }
}

# Point the rule at the lambda function. 
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_snapshot_cleanup.name
  arn       = aws_lambda_function.snapshot_cleanup.arn
  target_id = "${var.project_name}-daily-scheduler"
}

# Give EventBridge permission to invoke the lambda function.
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeToInvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.snapshot_cleanup.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_snapshot_cleanup.arn
}