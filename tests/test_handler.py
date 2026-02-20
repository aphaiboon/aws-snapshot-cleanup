import boto3
from botocore.exceptions import ClientError
import pytest
import os
from unittest.mock import patch, MagicMock
from moto import mock_aws
from datetime import datetime, timezone

from handler import handler


@mock_aws
def test_no_snapshots():
    """Exits cleanly when the account has no snapshots."""
    os.environ["CUTOFF_DAYS"] = "365"
    boto3.client("ec2", region_name="us-east-1")
    assert handler({}, {}) is None


@mock_aws
def test_no_old_snapshots():
    """Exits cleanly when all snapshots are newer than the cutoff."""
    os.environ["CUTOFF_DAYS"] = "365"
    ec2 = boto3.client("ec2", region_name="us-east-1")

    volume = ec2.create_volume(AvailabilityZone="us-east-1a", Size=1)
    ec2.create_snapshot(VolumeId=volume["VolumeId"], Description="Recent snapshot")

    assert handler({}, {}) is None


@mock_aws
def test_deletes_old_snapshots():
    """Deletes snapshots that are older than the cutoff and confirms they are gone."""
    os.environ["CUTOFF_DAYS"] = "0"
    ec2 = boto3.client("ec2", region_name="us-east-1")

    volume = ec2.create_volume(AvailabilityZone="us-east-1a", Size=1)
    snapshot = ec2.create_snapshot(VolumeId=volume["VolumeId"], Description="Old snapshot")
    snapshot_id = snapshot["SnapshotId"]

    assert ec2.describe_snapshots(SnapshotIds=[snapshot_id])["Snapshots"]

    handler({}, {})

    # Snapshot should no longer exist after the handler runs
    with pytest.raises(ClientError) as exc:
        ec2.describe_snapshots(SnapshotIds=[snapshot_id])
    assert "InvalidSnapshot.NotFound" in str(exc.value)


def test_delete_failure_continues():
    """Logs the error and keeps processing when a single delete fails."""
    os.environ["CUTOFF_DAYS"] = "0"

    with patch("handler.boto3") as mock_boto3:
        mock_ec2 = MagicMock()
        mock_boto3.client.return_value = mock_ec2

        mock_ec2.describe_snapshots.return_value = {
            "Snapshots": [
                {"SnapshotId": "snap-111", "StartTime": datetime.now(timezone.utc)},
                {"SnapshotId": "snap-222", "StartTime": datetime.now(timezone.utc)},
            ]
        }

        # First delete fails, second succeeds — handler should process both
        mock_ec2.delete_snapshot.side_effect = [
            ClientError(
                {"Error": {"Code": "InvalidSnapshot.InUse", "Message": "Snapshot in use"}},
                "DeleteSnapshot"
            ),
            None,
        ]

        handler({}, {})

        assert mock_ec2.delete_snapshot.call_count == 2
