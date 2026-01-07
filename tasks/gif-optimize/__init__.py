#region generated meta
import typing
class Inputs(typing.TypedDict):
    gif_path: str
    output_path: str | None
    optimize_level: typing.Literal[1, 2, 3] | None
    max_colors: int | None
    reduce_fps: int | None
class Outputs(typing.TypedDict):
    optimized_gif_path: typing.NotRequired[str]
    original_size: typing.NotRequired[int]
    optimized_size: typing.NotRequired[int]
    compression_ratio: typing.NotRequired[float]
#endregion

from oocana import Context
from PIL import Image
import os

def main(params: Inputs, context: Context) -> Outputs:
    """
    Optimize GIF file size by reducing colors and frames

    Args:
        params: Input parameters with gif_path, output_path, and optimization settings
        context: OOMOL context object

    Returns:
        Dictionary with optimized_gif_path, file sizes, and compression_ratio
    """
    gif_path = params["gif_path"]
    output_path = params.get("output_path") or os.path.join(context.session_dir, "optimized.gif")
    optimize_level = params.get("optimize_level")
    if optimize_level is None:
        optimize_level = 2  # Default: medium optimization
    max_colors = params.get("max_colors")
    if max_colors is None:
        max_colors = 256  # Default: no color reduction
    max_colors = max(2, min(256, max_colors))
    reduce_fps = params.get("reduce_fps")
    if reduce_fps is None:
        reduce_fps = 1  # Default: keep all frames
    reduce_fps = max(1, reduce_fps)

    # Get original file size
    original_size = os.path.getsize(gif_path)

    # Open GIF and extract frames
    with Image.open(gif_path) as gif:
        frames = []
        durations = []
        frame_index = 0

        try:
            while True:
                # Apply FPS reduction
                if frame_index % reduce_fps == 0:
                    current_frame = gif.copy()

                    # Reduce colors based on optimization level
                    if optimize_level >= 2:
                        # Convert to P mode with reduced palette
                        if current_frame.mode != 'P':
                            current_frame = current_frame.convert('RGB').convert(
                                'P',
                                palette=Image.Palette.ADAPTIVE,
                                colors=max_colors
                            )

                    frames.append(current_frame)

                    # Adjust duration for skipped frames
                    duration = gif.info.get('duration', 100) * reduce_fps
                    durations.append(duration)

                frame_index += 1
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

    if not frames:
        raise ValueError("No frames to optimize")

    # Save optimized GIF with appropriate settings
    save_kwargs = {
        'save_all': True,
        'append_images': frames[1:] if len(frames) > 1 else [],
        'duration': durations[0] if durations else 100,
        'loop': 0,
        'optimize': optimize_level >= 1
    }

    frames[0].save(output_path, **save_kwargs)

    # Get optimized file size
    optimized_size = os.path.getsize(output_path)
    compression_ratio = original_size / optimized_size if optimized_size > 0 else 1.0

    return {
        "optimized_gif_path": output_path,
        "original_size": original_size,
        "optimized_size": optimized_size,
        "compression_ratio": compression_ratio
    }
