import logging
import os
from datetime import datetime, timezone, timedelta
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    cutoff_days = int(os.environ.get("CUTOFF_DAYS", "365"))
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=cutoff_days)

    ec2 = boto3.client("ec2")

    # Only pull snapshots for the current account.
    response = ec2.describe_snapshots(OwnerIds=["self"])
    snapshots = response.get("Snapshots", [])

    if not snapshots:
        logger.info("No snapshots found")
        return

    # Filter snapshots older than the cutoff date.
    old_snapshots = [snapshot for snapshot in snapshots if snapshot["StartTime"] < cutoff_date]

    # If no snapshots are found, log and exit.
    if not old_snapshots:
        logger.info("No snapshots older than %d days found", cutoff_days)
        return

    logger.info("Found %d snapshots older than %d days. Starting cleanup...", len(old_snapshots), cutoff_days)

    # Iterate over the old snapshots and delete them.
    for snapshot in old_snapshots:
        snapshot_id = snapshot["SnapshotId"]

        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            logger.info("Deleting snapshot: %s", snapshot_id)
        except Exception as e:
            logger.error("Error deleting snapshot %s: %s", snapshot_id, e)
            continue

    logger.info("Cleanup completed. %d snapshots deleted.", len(old_snapshots))
    return