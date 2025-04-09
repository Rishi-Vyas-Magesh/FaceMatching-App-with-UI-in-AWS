# FaceMatching-App-with-UI-in-AWS

This is a fascinating project in which I have used my knowledge and Intrest in "Computer Vision" to come-up with a Limited Face recognition App which runs on an EC2 instance launced in AWS. Let me Explain with Brief Steps:

Step-1: I created an AWS free tier account where i have 1 year free access to use services.
Step-2: I collected images of 6 close people to me in different angles (10-15 images each) and sorted them.
Step-3: I stored these images in a bucket I created on S3 for all my now and future Images if I want to scale up.
Step-4: I logged in to AWS cloudshell CLI and created "FaceCollection" folder in AWS Rekognition where any folders with faces I index--the metadata,face Id,face embeddings etc will be stored---used the "IndexFaces" API
Step-5: I created 3 python Scripts--"index_faces"--Indexes the folder in my bucket with all images and attaches the folder name(person's name) as an "ExternalImageID". This will be ouput during rekognition because even if AWS indexes faces of same person, each image has a unique FaceID assigned.
Step:6 I created the "list_faces" code to check if all folders and images were indexed and "search_faces" code using the "SeachFacesByImage"API--It uses the image i upload--indexes it and compares it with the images information stored in "FaceCollection" to find a match. Then it outputs the "External Image ID" with a confidence score percentile.

(NOTE: I also created code to"index_new_faces" as they are added in my Images bucket---So that I can scale this.)

Step-7: I wanted to make it with a basic UI and application code. Hence, I launched an EC2 instance, with keys and security groups--Specific Inbound rules! to allow access from any IP address on port 5000.
Step-8: I created neccessary role and attached EC2,Rekognition.S3 full access to it and made the instance assume that role.
Step-9: I connected to the EC2 via my CLI and Instance Key---- I created my "app.py" code to use my work on the backend to do the FaceMatching LIKE i SAID and basic HTML code for a UI.-----I launched it in the IPV4 address of my code--- the UI opens.

Step-10: I can upload any image of a person part of my database/collection of Images and it will immediately identify and flag them!!! and In my testing It works.

(The codes and access and proof will be uploaded soon)
(The PPT with a business implication for such a model will also be uploaded soon)


