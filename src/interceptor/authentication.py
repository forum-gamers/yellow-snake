from grpc import ServerInterceptor, StatusCode, unary_unary_rpc_method_handler, ServicerContext
from src.helpers.jwt import verify_token


class Authentication(ServerInterceptor):
    def __init__(self) -> None:
        super().__init__()
        self.terminator = Authentication.unary_terminator(
            StatusCode.UNAUTHENTICATED, 'missing or invalid token')

    def intercept_service(self, continuation, handler_call_details: ServicerContext):
        try:
            metadata = dict(handler_call_details.invocation_metadata)
            access_token = metadata.get("access_token", [])
            if access_token is None or access_token == "":
                raise ValueError("missing or invalid token")

            claim = verify_token(access_token)
            new_meta = tuple(
                handler_call_details.invocation_metadata) + ('user', claim)

            return continuation(handler_call_details._replace(invocation_metadata=new_meta))
        except Exception:
            return self.terminator

    @staticmethod
    def unary_terminator(code, details):
        def terminate(ignored_request, context: ServicerContext):
            context.abort(code, details)

        return unary_unary_rpc_method_handler(terminate)
