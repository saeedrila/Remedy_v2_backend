from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import uuid
import os
import boto3
import tempfile
from botocore.exceptions import ClientError
import logging

from authentication.models import Account
from doctors_and_labs.models import DoctorProfile, LabProfile
from executives.models import ExecutiveProfile



def upload_to_s3(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
    try:
        # print('Entered upload_to try')
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print('Upload error: ', e)
        return False
    return True

class UploadProfileImage(APIView):
    def post(self, request):
        try:
            if 'profileImage' not in request.FILES:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = request.FILES['profileImage']    

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_name = temp_file.name

            unique_identifier = str(uuid.uuid4())
            unique_identifier_short = unique_identifier.replace("-", "")[:10]
            file_extension = uploaded_file.name.split('.')[-1]
            new_file_name = f'{unique_identifier_short}.{file_extension}'

            logging.getLogger('django').debug('Starting file upload process')
            logging.getLogger('django').debug(f'Uploaded file: {uploaded_file.name}')
            logging.getLogger('django').debug(f'New file name: {new_file_name}')


            file_directory_within_bucket = 'media/profile_pic'
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                new_file_name
            )

            logging.getLogger('django').debug(f'File path within bucket: {file_path_within_bucket}')

            response = upload_to_s3(temp_file_name, settings.AWS_STORAGE_BUCKET_NAME, file_path_within_bucket)
            logging.getLogger('django').debug('File upload process completed')
            os.remove(temp_file_name)
            aws_public_url = 'https://remedy-development.s3.ap-south-1.amazonaws.com'
            profile_public_url = os.path.join(
                aws_public_url,
                file_path_within_bucket
            )
            try:
                account_obj = Account.objects.get(email = request.user.email)
                account_obj.profile_pic_url = file_path_within_bucket
                account_obj.save()
                print('url saved to database')
            except:
                print('Request', request.user)
                print('Could not get account and did not saved to database')

            print('Public URL: ', profile_public_url)
            response_data = {
                'message': 'File uploaded and saved successfully',
                'profilePublicUrl': profile_public_url,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.getLogger('django').error('An error occurred during file upload: %s', str(e))
            return Response({'error': 'An error occurred while processing the file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UploadDocument(APIView):
    def post(self, request):
        try:
            if 'document' not in request.FILES:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = request.FILES['document']    

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_name = temp_file.name

            unique_identifier = str(uuid.uuid4())
            unique_identifier_short = unique_identifier.replace("-", "")[:10]
            file_extension = uploaded_file.name.split('.')[-1]
            new_file_name = f'doc_{unique_identifier_short}.{file_extension}'

            logging.getLogger('django').debug('Starting file upload process')
            logging.getLogger('django').debug(f'Uploaded file: {uploaded_file.name}')
            logging.getLogger('django').debug(f'New file name: {new_file_name}')


            file_directory_within_bucket = 'media/docs'
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                new_file_name
            )

            logging.getLogger('django').debug(f'File path within bucket: {file_path_within_bucket}')

            response = upload_to_s3(temp_file_name, settings.AWS_STORAGE_BUCKET_NAME, file_path_within_bucket)
            logging.getLogger('django').debug('File upload process completed')
            os.remove(temp_file_name)
            aws_public_url = 'https://remedy-development.s3.ap-south-1.amazonaws.com'
            document_public_url = os.path.join(
                aws_public_url,
                file_path_within_bucket
            )

            def save_document_url(request, profile_model):
                try:
                    account_obj = Account.objects.get(email=request.user.email)
                    role_field = None
                    if request.user.is_executive:
                        role_field = 'executive'
                    elif request.user.is_doctor:
                        role_field = 'doctor'
                    elif request.user.is_lab:
                        role_field = 'lab'

                    if role_field is not None:
                        profile_obj = profile_model.objects.get(**{role_field: account_obj})
                        profile_obj.document_url = file_path_within_bucket
                        profile_obj.save()
                        print('URL saved to the database')
                    else:
                        print('Could not determine account role')   
                except Account.DoesNotExist:
                    print('Account does not exist for:', request.user.email)
                except profile_model.DoesNotExist:
                    print(f'{profile_model.__name__} does not exist for the corresponding account')
                except Exception as e:
                    print('An unexpected error occurred:', str(e))

            if request.user.is_executive:
                save_document_url(request, ExecutiveProfile)
            elif request.user.is_doctor:
                save_document_url(request, DoctorProfile)
            elif request.user.is_lab:
                save_document_url(request, LabProfile)
            else:
                print('Could not get account role')

            print('Public URL: ', document_public_url)
            response_data = {
                'message': 'File uploaded and saved successfully',
                'profilePublicUrl': document_public_url,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.getLogger('django').error('An error occurred during file upload: %s', str(e))
            return Response({'error': 'An error occurred while processing the file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        