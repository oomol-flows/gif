#region generated meta
import typing
class Inputs(typing.TypedDict):
    gif_path: str
    output_path: str | None
    speed_multiplier: float | None
    fps: float | None
class Outputs(typing.TypedDict):
    adjusted_gif_path: typing.NotRequired[str]
    original_duration: typing.NotRequired[float]
    new_duration: typing.NotRequired[float]
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Adjust GIF playback speed by FPS or multiplier

    Args:
        params: Input parameters with gif_path, output_path, speed_multiplier, and fps
        context: OOMOL context object

    Returns:
        Dictionary with adjusted_gif_path, original_duration, and new_duration
    """
    gif_path = params["gif_path"]
    output_path = params.get("output_path") or os.path.join(context.session_dir, "speed_adjusted.gif")
    speed_multiplier = params.get("speed_multiplier")
    if speed_multiplier is None:
        speed_multiplier = 1.0  # Default: no speed change
    target_fps = params.get("fps")
    if target_fps is None:
        target_fps = 0  # Default: use speed_multiplier instead

    # Open GIF and extract frames
    with Image.open(gif_path) as gif:
        original_duration = gif.info.get('duration', 100)

        # Calculate new duration
        if target_fps > 0:
            # Use FPS to calculate duration (FPS = 1000ms / duration)
            new_duration = int(1000 / target_fps)
        else:
            # Use speed multiplier (faster = shorter duration)
            new_duration = int(original_duration / speed_multiplier)

        # Ensure minimum duration of 1ms
        new_duration = max(1, new_duration)

        # Extract all frames
        frames = []
        try:
            while True:
                frames.append(gif.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Save with new duration
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=new_duration,
            loop=gif.info.get('loop', 0),
            optimize=False
        )

    return {
        "adjusted_gif_path": output_path,
        "original_duration": float(original_duration),
        "new_duration": float(new_duration)
    }
