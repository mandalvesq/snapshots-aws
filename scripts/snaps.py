import boto3
import json
import os

account_source = os.environ['account_source']
account_destination = os.environ['account_destination']
bucket = os.environ['bucket']

ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3')


def get_snapshots():
    response = ec2.describe_snapshots(OwnerIds=[account_source])
    return response

def transfer_snaps(response):
    for snapshots in response['Snapshots']:
        encript = snapshots['Encrypted']

        if encript is False:
            snap = snapshots['SnapshotId']
            print('Moving Snapshot ID -> ' + snap + ' from ' + account_source + ' to ' + account_destination)
            ec2_snap = boto3.resource('ec2')
            conn = ec2_snap.Snapshot(snap)
            move_snap = conn.modify_attribute(
                Attribute='createVolumePermission',
                OperationType='add',
                UserIds=[account_destination]
                )
        else:
            print('Encripted snapshots will be transfered later')
        
    
def get_tags(response):
    all_tags = []
    for snapshot in response['Snapshots']:
        if 'Tags' in snapshot:
            for tag in snapshot['Tags']:
                all_tags.append({snapshot['SnapshotId'] : {tag['Key']: tag['Value']}})

    return all_tags


def upload_history(result, bucket):
    key = 'history/snaps.json'
    print('Uploading history to S3') 
    s3.put_object(
        Body=json.dumps(result),
        Bucket=bucket,
        Key=key
    )

if __name__ == '__main__':
    response = get_snapshots()
    transfer_snaps(response)
    all_tags = get_tags(response)
    upload_history(all_tags, bucket)
