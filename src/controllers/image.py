from grpc import ServicerContext, RpcError, StatusCode
from image_pb2 import UploadFileResult, Message, MultipleUploadFileResult
from src.helpers.file import check_file_ext, check_file_size
from src.lib.imagekit import Upload
from image_pb2_grpc import ImageServicer
from imagekitio.client import UpdateFileRequestOptions


class ImageService(ImageServicer):
    def __init__(self, upload_lib: Upload) -> None:
        super().__init__()
        self.upload_service = upload_lib

    def UploadImg(self, request, context: ServicerContext):
        if request.content == "" or request.content is None or request.filename == "" or request.filename is None or request.folder == "" or request.folder is None:
            raise RpcError(StatusCode.INVALID_ARGUMENT, "invalid parameter")

        if not check_file_size(len(request.content)):
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "maximum file size upload"
            )

        file_type = check_file_ext(request.filename)
        if file_type is None:
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "unsupported file extension"
            )

        opts = UpdateFileRequestOptions()
        opts.folder = request.folder
        resp = self.upload_service.upload_file(
            request.content, request.filename, opts
        )

        return UploadFileResult(file_id=resp.file_id, name=resp.name, url=resp.url, content_type=file_type)

    def DeleteFile(self, request, context: ServicerContext):
        if request.file_id == None or request.file_id == "":
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "no file_id provided"
            )

        self.upload_service.delete_file(request.file_id)

        return Message(message='success')

    def BulkUpload(self, request, context: ServicerContext):
        if request.files is None or len(request.files) < 1:
            raise RpcError(StatusCode.INVALID_ARGUMENT, "invalid parameter")

        valid_files = []
        for file in request.files:
            if not check_file_size(len(file.content)):
                continue

            file_type = check_file_ext(file.filename)
            if file_type is None:
                continue

            valid_files.append(
                {'url': file.content, 'file_name': file.filename, 'file_type': file_type})

        if len(valid_files) < 1:
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "no valid file provided"
            )

        opts = UpdateFileRequestOptions()
        opts.folder = request.folder

        datas = self.upload_service.bulk_upload_file(valid_files, opts)
        results = [
            {'file_id': data.file_id, 'name': data.name,
                'content_type': check_file_ext(data.name), 'url': data.url}
            for data in datas
        ]
        return MultipleUploadFileResult(datas=results)

    def BulkDeleteFile(self, request, context: ServicerContext):
        if len(request.file_ids) < 1:
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "no file_ids provided"
            )

        self.upload_service.bulk_delete_file(file_ids=request.file_ids)

        return Message(message='success')
