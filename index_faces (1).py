import boto3
import re

# Initialize AWS clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# Fixed project values
bucket_name = 'aws-ml-proj-bucket'
collection_id = 'FaceCollection'

# Function to sanitize ExternalImageId to match AWS naming rules
def sanitize_external_id(name):
    return re.sub(r'[^a-zA-Z0-9_.\-:]', '_', name)

# Go through every object in the bucket
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

print(f"\n🔍 Scanning S3 bucket: {bucket_name}...\n")

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            file_key = obj['Key']

            # Only process image files
            if file_key.lower().endswith(('.jpg', '.jpeg', '.png')):

                # Get folder name as class label
                path_parts = file_key.split('/')
                if len(path_parts) >= 2:
                    folder_name = path_parts[0]
                else:
                    print(f"⚠️ Skipping file (not inside a folder): {file_key}")
                    continue

                # Sanitize folder name
                external_image_id = sanitize_external_id(folder_name)

                print(f"📂 Indexing: {file_key} ➜ ExternalImageId: '{external_image_id}'")

                try:
                    response = rekognition.index_faces(
                        CollectionId=collection_id,
                        Image={
                            'S3Object': {
                                'Bucket': bucket_name,
                                'Name': file_key
                            }
                        },
                        ExternalImageId=external_image_id,
                        DetectionAttributes=['ALL']
                    )
                    print(f"✅ Indexed successfully: {file_key}\n")

                except Exception as e:
                    print(f"❌ Error indexing {file_key}: {e}\n")

