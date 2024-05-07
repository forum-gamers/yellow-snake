from grpc import ServicerContext, RpcError, StatusCode
from image_pb2 import UploadFileResult, Message
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

        fileType = check_file_ext(request.filename)
        if fileType is None:
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "unsupported file extension"
            )

        opts = UpdateFileRequestOptions()
        opts.folder = request.folder
        resp = self.upload_service.upload_file(
            request.content, request.filename, opts
        )

        return UploadFileResult(file_id=resp.file_id, name=resp.name, url=resp.url, content_type=fileType)

    def DeleteFile(self, request, context: ServicerContext):
        if request.file_id == None or request.file_id == "":
            raise RpcError(
                StatusCode.INVALID_ARGUMENT,
                "no file_id provided"
            )

        self.upload_service.delete_file(request.file_id)

        return Message(message='success')
