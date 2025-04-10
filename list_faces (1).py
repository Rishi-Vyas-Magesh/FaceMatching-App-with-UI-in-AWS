import boto3

# AWS Rekognition client
rekognition = boto3.client('rekognition')

collection_id = 'FaceCollection'

print(f"\n📂 Listing all faces in collection: {collection_id}\n")

response = rekognition.list_faces(CollectionId=collection_id)

faces = response['Faces']

if not faces:
    print("❌ No faces found in the collection.")
else:
    for face in faces:
        print(f"🧑 FaceId: {face['FaceId']}")
        print(f"🔖 ExternalImageId: {face['ExternalImageId']}")
        print(f"🖼️ ImageId: {face['ImageId']}")
        print('-' * 40)

# Handle pagination if there are many faces
while 'NextToken' in response:
    response = rekognition.list_faces(
        CollectionId=collection_id,
        NextToken=response['NextToken']
    )
    for face in response['Faces']:
        print(f"🧑 FaceId: {face['FaceId']}")
        print(f"🔖 ExternalImageId: {face['ExternalImageId']}")
        print(f"🖼️ ImageId: {face['ImageId']}")
        print('-' * 40)

