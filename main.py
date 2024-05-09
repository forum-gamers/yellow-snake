import grpc
import image_pb2_grpc as grpcImageService
from src.controllers.image import ImageService
from src.lib.imagekit import Upload
import concurrent.futures
from src.interceptor.logging import Logging
from src.interceptor.authentication import Authentication
import logging


def serve():
    server = grpc.server(
        thread_pool=concurrent.futures.ThreadPoolExecutor(max_workers=10),
        handlers=None,
        interceptors=(
            Logging(), Authentication()
        )
    )
    upload = Upload()
    grpcImageService.add_ImageServicer_to_server(
        ImageService(upload_lib=upload), server)
    port = "50060"
    server.add_insecure_port('[::]:'+port)

    print('server starting on port '+port+' ...')
    server.start()
    print('server started')
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
