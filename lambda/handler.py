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
    snapshots = ec2.describe_snapshots(OwnerIds=["self"]).get("Snapshots", [])

    if not snapshots:
        logger.info("No snapshots found")
        return

    old_snapshots = [s for s in snapshots if s["StartTime"] < cutoff_date]

    if not old_snapshots:
        logger.info("No snapshots older than %d days found", cutoff_days)
        return

    logger.info("Found %d snapshots older than %d days. Starting cleanup...", len(old_snapshots), cutoff_days)

    for snapshot in old_snapshots:
        snapshot_id = snapshot["SnapshotId"]
        try:
            logger.info("Deleting snapshot: %s", snapshot_id)
            ec2.delete_snapshot(SnapshotId=snapshot_id)
        except Exception as e:
            logger.error("Failed to delete snapshot %s: %s", snapshot_id, e)

    logger.info("Cleanup complete. %d snapshots deleted.", len(old_snapshots))
