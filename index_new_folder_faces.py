import boto3
import re
import os

# AWS clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# Your project settings
bucket_name = 'aws-ml-proj-bucket'
collection_id = 'FaceCollection'
tracking_file = 'indexed_folders.txt'

# Load already indexed folders
if os.path.exists(tracking_file):
    with open(tracking_file, 'r') as f:
        indexed_folders = set(line.strip() for line in f)
else:
    indexed_folders = set()

# Function to clean ExternalImageId
def sanitize_external_id(name):
    return re.sub(r'[^a-zA-Z0-9_.\-:]', '_', name)

# List folders in S3
response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')
folders = [prefix['Prefix'].rstrip('/') for prefix in response.get('CommonPrefixes', [])]

new_folders = [f for f in folders if f not in indexed_folders]

print(f"📁 New folders to index: {new_folders}")

for folder in new_folders:
    safe_id = sanitize_external_id(folder)
    print(f"\n🔄 Indexing faces for: {folder} ➜ '{safe_id}'")

    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder + '/')
    for obj in objects.get('Contents', []):
        file_key = obj['Key']

        if file_key.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"📤 Indexing: {file_key}")
            try:
                rekognition.index_faces(
                    CollectionId=collection_id,
                    Image={'S3Object': {'Bucket': bucket_name, 'Name': file_key}},
                    ExternalImageId=safe_id,
                    DetectionAttributes=['DEFAULT']
                )
            except Exception as e:
                print(f"❌ Error indexing {file_key}: {e}")

    # ✅ Add folder to the tracking file
    with open(tracking_file, 'a') as f:
        f.write(folder + '\n')

print("\n✅ Indexing complete. Only new folders were processed.")

