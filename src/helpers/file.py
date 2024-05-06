import os


def check_file_ext(filename: str) -> str | None:
    ext = os.path.splitext(filename)[1][1:]

    for img_ext in ["png", "jpg", "jpeg", "gif", "bmp"]:
        if img_ext == ext:
            return "image"

    for vid_ext in ["mp4", "avi", "mkv", "mov"]:
        if vid_ext == ext:
            return "video"

    return None


def check_file_size(size: int) -> bool:
    return size < 10 * 1024 * 1024
