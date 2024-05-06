import grpc
import image_pb2_grpc as grpcImageService
from src.controllers.image import ImageService
from src.lib.imagekit import Upload


def serve():
    server = grpc.server(thread_pool=10)
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
    serve()
