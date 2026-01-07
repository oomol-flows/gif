#region generated meta
import typing
class Inputs(typing.TypedDict):
    gif_path: str
    output_path: str | None
    width: int | None
    height: int | None
    scale_percent: float | None
    resample_method: typing.Literal["LANCZOS", "BILINEAR", "BICUBIC", "NEAREST"] | None
class Outputs(typing.TypedDict):
    resized_gif_path: typing.NotRequired[str]
    original_size: typing.NotRequired[list[int]]
    new_size: typing.NotRequired[list[int]]
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Resize GIF animation by dimensions or percentage

    Args:
        params: Input parameters with gif_path, output_path, dimensions, and scale
        context: OOMOL context object

    Returns:
        Dictionary with resized_gif_path, original_size, and new_size
    """
    gif_path = params["gif_path"]
    output_path = params.get("output_path") or os.path.join(context.session_dir, "resized.gif")
    target_width = params.get("width") or 0
    target_height = params.get("height") or 0
    scale_percent = params.get("scale_percent") or 100  # Default: 100% (no scaling)
    resample_method = params.get("resample_method") or "LANCZOS"  # Default: highest quality

    # Map resample method string to PIL constant
    resample_map = {
        "LANCZOS": Image.Resampling.LANCZOS,
        "BILINEAR": Image.Resampling.BILINEAR,
        "BICUBIC": Image.Resampling.BICUBIC,
        "NEAREST": Image.Resampling.NEAREST
    }
    resample = resample_map.get(resample_method, Image.Resampling.LANCZOS)

    # Open GIF and get original size
    with Image.open(gif_path) as gif:
        original_width, original_height = gif.size

        # Calculate new dimensions
        if target_width > 0 and target_height > 0:
            # Both dimensions specified
            new_width, new_height = target_width, target_height
        elif target_width > 0:
            # Only width specified, maintain aspect ratio
            new_width = target_width
            new_height = int(original_height * (target_width / original_width))
        elif target_height > 0:
            # Only height specified, maintain aspect ratio
            new_height = target_height
            new_width = int(original_width * (target_height / original_height))
        else:
            # Use scale percentage
            new_width = int(original_width * scale_percent / 100)
            new_height = int(original_height * scale_percent / 100)

        # Process all frames
        frames = []
        durations = []

        try:
            while True:
                # Resize current frame
                resized_frame = gif.resize((new_width, new_height), resample)
                frames.append(resized_frame.copy())
                durations.append(gif.info.get('duration', 100))

                # Move to next frame
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Save resized GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations[0],
            loop=gif.info.get('loop', 0),
            optimize=False
        )

    return {
        "resized_gif_path": output_path,
        "original_size": [original_width, original_height],
        "new_size": [new_width, new_height]
    }
