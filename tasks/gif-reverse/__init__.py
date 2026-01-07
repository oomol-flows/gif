#region generated meta
import typing
class Inputs(typing.TypedDict):
    gif_path: str
    output_path: str | None
class Outputs(typing.TypedDict):
    reversed_gif_path: typing.NotRequired[str]
    frame_count: typing.NotRequired[int]
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Reverse the playback order of GIF frames

    Args:
        params: Input parameters with gif_path and output_path
        context: OOMOL context object

    Returns:
        Dictionary with reversed_gif_path and frame_count
    """
    gif_path = params["gif_path"]
    output_path = params.get("output_path") or os.path.join(context.session_dir, "reversed.gif")

    # Open GIF and extract all frames
    with Image.open(gif_path) as gif:
        frames = []
        durations = []

        try:
            while True:
                frames.append(gif.copy())
                durations.append(gif.info.get('duration', 100))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        # Reverse frames and durations
        frames.reverse()
        durations.reverse()

        # Save reversed GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations[0],
            loop=gif.info.get('loop', 0),
            optimize=False
        )

    return {
        "reversed_gif_path": output_path,
        "frame_count": len(frames)
    }
