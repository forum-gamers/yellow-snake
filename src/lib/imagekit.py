from typing import List
from src.conf.environment import value
from imagekitio.client import (
    ImageKit,
    UpdateFileRequestOptions,
    UploadFileResult,
    ResponseMetadataResult,
    BulkDeleteFileResult
)


class Upload:
    def __init__(self):
        self.client = ImageKit(
            public_key=value.get('IMAGEKIT_PUBLIC_KEY'),
            private_key=value.get('IMAGEKIT_PRIVATE_KEY'),
            url_endpoint=value.get('IMAGEKIT_URL')
        )

    def upload_file(
        self,
        url: str | List[int],
        filename: str,
        opts: UpdateFileRequestOptions | None
    ) -> UploadFileResult:
        return self.client.upload(file=url, file_name=filename, options=opts)

    def delete_file(self, file_id: str) -> ResponseMetadataResult:
        return self.client.delete_file(file_id)

    def bulk_delete_file(self, file_ids: List[str]) -> BulkDeleteFileResult:
        return self.client.bulk_file_delete(file_ids)
