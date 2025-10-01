#region generated meta
import typing

class Inputs(typing.TypedDict):
    image_paths: list[str]
    output_path: str
    duration: float
    loop: int

class Outputs(typing.TypedDict):
    gif_path: str
    frame_count: int
    file_size: int
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Combine multiple images into an animated GIF

    Args:
        params: Input parameters containing image_paths, output_path, duration, and loop
        context: OOMOL context object

    Returns:
        Dictionary with gif_path, frame_count, and file_size
    """
    image_paths = params["image_paths"]
    output_path = params["output_path"]
    duration = int(params["duration"])
    loop = params["loop"]

    if not image_paths:
        raise ValueError("No images provided to compose GIF")

    # Load all images
    frames = []
    for img_path in image_paths:
        img = Image.open(img_path)
        # Convert to RGBA to ensure consistency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        frames.append(img)

    # Save as GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=False
    )

    # Get file size
    file_size = os.path.getsize(output_path)

    return {
        "gif_path": output_path,
        "frame_count": len(frames),
        "file_size": file_size
    }
