from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import HttpResponseBadRequest
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from ShareApp.permissions import IsOpsUser
from ShareApp.utils import is_valid_file
import hashlib
import hmac
import time
import base64
from django.conf import settings
import os
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from ShareApp.permissions import IsOpsUser,IsClientUser

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated, IsOpsUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.data.get('file')

        # Check if file is provided
        if not file:
            return HttpResponseBadRequest("No file uploaded.")

        # Validate file type
        if not is_valid_file(file.name):
            return Response({"error": "Invalid file type. Only pptx, docx, and xlsx are allowed."}, status=400)

        # Save file
        uploaded_file = UploadedFile.objects.create(file=file)
        return Response({"message": "File uploaded successfully.", "file_id": uploaded_file.id}, status=201)

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated,IsClientUser]

    def generate_encrypted_url(self, assignment_id):
        secret_key = settings.SECRET_KEY.encode()
        expiration_time = int(time.time()) + 300  # URL valid for 5 minutes

        # Create a message with assignment ID and expiration time
        message = f"{assignment_id}:{expiration_time}".encode()

        # Generate HMAC signature
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

        # Encode assignment ID, timestamp, and signature as a single string
        data = f"{assignment_id}:{expiration_time}:{signature}"
        encrypted_data = base64.urlsafe_b64encode(data.encode()).decode()

        # Construct the download URL
        return f"localhost:8000/files/download-file/{encrypted_data}"

    def get(self, request, assignment_id):
        # Check if the file exists
        try:
            uploaded_file = UploadedFile.objects.get(id=assignment_id)
        except UploadedFile.DoesNotExist:
            return Response({"error": "404 Not found"}, status=404)

        # Generate encrypted download link
        download_link = self.generate_encrypted_url(assignment_id)

        # Respond with the download link
        return Response({
            "download-link":download_link ,
            "message": "success"
        }, status=200)


class DownloadFileView(APIView):
    # permission_classes = [IsAuthenticated,IsClientUser]
    permission_classes = [AllowAny]

    def get(self, request, encrypted_data):
       
        # Decode the encrypted data
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode()).decode()
            assignment_id, timestamp, signature = decoded_data.split(":")
        except (ValueError, base64.binascii.Error):
            return HttpResponseBadRequest("Invalid download link.")

        # Verify timestamp
        current_time = int(time.time())
        if current_time > int(timestamp):
            return HttpResponseBadRequest("The download link has expired.")

        # Verify HMAC signature
        secret_key = settings.SECRET_KEY.encode()
        message = f"{assignment_id}:{timestamp}".encode()
        expected_signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return HttpResponseBadRequest("Invalid download link.")

        # Fetch the file
        try:
            uploaded_file = UploadedFile.objects.get(id=assignment_id)
        except UploadedFile.DoesNotExist:
            return Http404("File not found.")

        # Serve the file for download
        response = HttpResponse(uploaded_file.file, content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={uploaded_file.file.name}"
        return response

class FileListView(APIView):
    permission_classes = [IsAuthenticated,IsClientUser]
    def get(self, request):
        # Get only the required fields
        files = UploadedFile.objects.all().values('file', 'uploaded_at')

        # Prepare a response with file details
        file_list = [{"file_name": os.path.basename(file['file']), "uploaded_at": file['uploaded_at']} for file in files]

        return Response({
            "files": file_list,
            "message": "success"
        }, status=200)