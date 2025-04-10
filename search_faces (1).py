import boto3

# ✅ Initialize Rekognition client
rekognition = boto3.client('rekognition')

# ✅ Specify the face collection you've already created
collection_id = 'FaceCollection'

# ✅ Ask the user for the test image file name
local_image_path = input("🖼️ Enter the test image filename :").strip()

try:
    # ✅ Open and read the image file as bytes
    with open(local_image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # ✅ Call Rekognition to search for the face
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        MaxFaces=1,  # Top match
        FaceMatchThreshold=90
    )

    matches = response.get('FaceMatches', [])

    if matches:
        print("\n✅ Match found!")
        for match in matches:
            print(f"Matched Face ID      : {match['Face']['FaceId']}")
            print(f"Matched Person (Name): {match['Face']['ExternalImageId']}")
            print(f"Confidence Score     : {match['Similarity']:.2f}%")
    else:
        print("\n❌ No match found. Try another image or lower the threshold.")

except FileNotFoundError:
    print(f"\n⚠️ File '{local_image_path}' not found in CloudShell. Upload the image and try again.")
except Exception as e:
    print(f"\n❌ Error occurred: {e}")

