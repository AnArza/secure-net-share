import os
import gzip

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.http import HttpResponse

from .models import File
from .serializers import FileSerializer, FileShareSerializer


class FileUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    chunk_size = 1024 * 1024 * 5  # 5 MB per chunk

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_instance = File(owner=request.user, name=uploaded_file.name, is_chunked=False)

        # Handle chunking and compression
        if uploaded_file.size > self.chunk_size:
            file_instance.is_chunked = True
            file_instance.save()
            base_path = f'media/uploads/{file_instance.id}/'
            os.makedirs(base_path, exist_ok=True)

            total_size_read = 0
            part_number = 0
            while total_size_read < uploaded_file.size:
                chunk = uploaded_file.file.read(self.chunk_size)
                if not chunk:
                    break
                compressed_chunk = gzip.compress(chunk)
                chunk_file_path = os.path.join(base_path, f'part_{part_number + 1}.gz')
                with open(chunk_file_path, 'wb') as f:
                    f.write(compressed_chunk)
                total_size_read += len(chunk)
                part_number += 1
        else:
            compressed_data = gzip.compress(uploaded_file.read())
            file_instance.file.save(f"{uploaded_file.name}.gz", ContentFile(compressed_data))

        file_instance.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "file_updates",
            {
                "type": "file.uploaded",
                "file": FileSerializer(file_instance).data  # Make sure the serializer outputs necessary data
            }
        )

        return Response(FileSerializer(file_instance).data, status=status.HTTP_201_CREATED)


class FileDownloadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, file_id):
        file_instance = File.objects.get(id=file_id)
        if not request.user == file_instance.owner and not request.user in file_instance.shared_with.all():
            return Response({'message': 'You do not have permission to access this file.'}, status=status.HTTP_403_FORBIDDEN)

        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'

        if file_instance.is_chunked:
            base_path = f'media/uploads/{file_instance.id}/'
            part_number = 1
            while True:
                chunk_file_path = os.path.join(base_path, f'part_{part_number}.gz')
                if not os.path.exists(chunk_file_path):
                    break
                with open(chunk_file_path, 'rb') as f:
                    decompressed_chunk = gzip.decompress(f.read())
                    response.write(decompressed_chunk)
                part_number += 1
        else:
            with open(file_instance.file.path, 'rb') as f:
                decompressed_content = gzip.decompress(f.read())
                response.write(decompressed_content)


        return response


class FileShareView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        with transaction.atomic():
            files = File.objects.filter(owner=request.user).exclude(shared_with__username__in=request.data['shared_with'])
            updated_files = []
            errors = []

            for file in files:
                serializer = FileShareSerializer(file, data=request.data, partial=True)
                if serializer.is_valid():
                    updated_file = serializer.save()
                    updated_files.append(updated_file)
                else:
                    errors.append(serializer.errors)

            if errors:
                return Response(errors[0], status=status.HTTP_400_BAD_REQUEST)

            # Notify users about the file update via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "file_updates",
                {
                    "type": "file_updated",
                    "files": FileSerializer(updated_files, many=True).data  # Sending updates for all files
                }
            )

        # If everything goes well, return a success message
        return Response({"message": "Files shared successfully."}, status=status.HTTP_200_OK)
