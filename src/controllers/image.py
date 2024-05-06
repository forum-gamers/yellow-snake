from grpc import ServicerContext, RpcError, StatusCode
from image_pb2 import UploadFileResult
from src.helpers.file import check_file_ext, check_file_size
from src.lib.imagekit import Upload
from image_pb2_grpc import ImageServicer


class ImageService(ImageServicer):
    def __init__(self, upload_lib: Upload) -> None:
        super().__init__()
        self.upload_service = upload_lib

    def UploadImg(self, request, context: ServicerContext):
        if not check_file_size(request.size):
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

        resp = self.upload_service.upload_file(
            request.content, fileType + "/" + request.filename
        )

        return UploadFileResult(file_id=resp.file_id, name=resp.name, url=resp.url)
