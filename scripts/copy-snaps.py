import boto3
import json
import os

account_source = os.environ['account_source']
region_source = os.environ['region_source']
region_destination = os.environ['region_destination']

ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.resource('s3')


def get_snapshots():
    response = ec2.describe_snapshots(OwnerIds=[account_source])
    return response

def copy_snaps(response):
    for snapshots in response['Snapshots']:
        snap = snapshots['SnapshotId']
        print('Coping Snapshot ID -> ' + snap)
        copy_snap = ec2.copy_snapshot(
        Description='Snapshot copied from' + snapshots['SnapshotId'],
        DestinationRegion=region_source,
        SourceRegion=region_destination,
        SourceSnapshotId=snapshots['SnapshotId'],
    )
    

if __name__ == '__main__':
    response = get_snapshots()
    copy_snaps(response)
