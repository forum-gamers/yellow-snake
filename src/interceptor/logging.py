from grpc import ServerInterceptor


class Logging(ServerInterceptor):
    def __init__(self) -> None:
        super().__init__()

    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method.split('/')[-1]
        print(f"request : {method_name}")

        return continuation(handler_call_details)
