#region generated meta
import typing
class Inputs(typing.TypedDict):
    gif_path: str
    width: int
    height: int
    output_path: str | None
    x: int | None
    y: int | None
class Outputs(typing.TypedDict):
    cropped_gif_path: typing.NotRequired[str]
    original_size: typing.NotRequired[list[int]]
    crop_area: typing.NotRequired[list[int]]
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Crop GIF animation to a specified rectangular area

    Args:
        params: Input parameters with gif_path, output_path, and crop coordinates
        context: OOMOL context object

    Returns:
        Dictionary with cropped_gif_path, original_size, and crop_area
    """
    gif_path = params["gif_path"]
    width = params["width"]
    height = params["height"]
    output_path = params.get("output_path") or os.path.join(context.session_dir, "cropped.gif")
    x = params.get("x")
    if x is None:
        x = 0  # Default: crop from top-left
    y = params.get("y")
    if y is None:
        y = 0  # Default: crop from top-left

    # Calculate crop box (left, upper, right, lower)
    crop_box = (x, y, x + width, y + height)

    # Open GIF and extract frames
    with Image.open(gif_path) as gif:
        original_width, original_height = gif.size

        # Validate crop area
        if x < 0 or y < 0 or x + width > original_width or y + height > original_height:
            raise ValueError(
                f"Crop area ({x}, {y}, {width}, {height}) exceeds "
                f"image boundaries ({original_width}x{original_height})"
            )

        frames = []
        durations = []

        try:
            while True:
                # Crop current frame
                cropped_frame = gif.crop(crop_box)
                frames.append(cropped_frame.copy())
                durations.append(gif.info.get('duration', 100))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Save cropped GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations[0],
            loop=gif.info.get('loop', 0),
            optimize=False
        )

    return {
        "cropped_gif_path": output_path,
        "original_size": [original_width, original_height],
        "crop_area": [x, y, width, height]
    }
