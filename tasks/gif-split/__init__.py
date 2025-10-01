#region generated meta
import typing

class Inputs(typing.TypedDict):
    gif_path: str
    output_dir: str
    format: str

class Outputs(typing.TypedDict):
    frame_paths: list[str]
    frame_count: int
    duration: float
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Extract individual frames from a GIF animation

    Args:
        params: Input parameters containing gif_path, output_dir, and format
        context: OOMOL context object

    Returns:
        Dictionary with frame_paths, frame_count, and duration
    """
    gif_path = params["gif_path"]
    output_dir = params["output_dir"]
    image_format = params["format"]

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the GIF
    with Image.open(gif_path) as gif:
        frame_paths = []
        frame_count = 0
        duration = gif.info.get('duration', 100)  # Default 100ms if not specified

        # Extract each frame
        try:
            while True:
                # Save current frame
                frame_filename = f"frame_{frame_count:04d}.{image_format}"
                frame_path = os.path.join(output_dir, frame_filename)

                # Convert RGBA to RGB if saving as JPG
                if image_format.lower() == 'jpg':
                    rgb_frame = gif.convert('RGB')
                    rgb_frame.save(frame_path, image_format.upper())
                else:
                    gif.save(frame_path, image_format.upper())

                frame_paths.append(frame_path)
                frame_count += 1

                # Move to next frame
                gif.seek(gif.tell() + 1)
        except EOFError:
            # End of frames
            pass

    return {
        "frame_paths": frame_paths,
        "frame_count": frame_count,
        "duration": float(duration)
    }
