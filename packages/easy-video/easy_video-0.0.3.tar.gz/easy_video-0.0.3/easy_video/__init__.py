"""Initialize published package."""

from easy_video.video import VideoReader, VideoWriter, _VideoRIdx, open_video

############## EDIT THESE INFORMATION ###############
AUTHOR = "Tamon Mikawa"
EMAIL = "mtamon.engineering@gmail.com"
YEAR = "2023"
GIT_URL = "https://github.com/MTamon/VideoTools.git"
VERSION = "0.0.3"
LICENCE = "MIT License"
#####################################################

__copyright__ = f"Copyright (C) {YEAR} {AUTHOR}"
__version__ = VERSION
__license__ = LICENCE
__author__ = AUTHOR
__author_email__ = EMAIL
__url__ = GIT_URL

__all__ = ["VideoReader", "VideoWriter", "open_video", "_VideoRIdx"]
