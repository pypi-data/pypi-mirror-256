from __future__ import annotations

import os
import re
import subprocess
from functools import cached_property

from yutto.utils.console.logger import Logger
from yutto.utils.funcutils import Singleton


class FFmpegNotFoundError(Exception):
    def __init__(self):
        super().__init__("请配置正确的 FFmpeg 路径")


class FFmpeg(metaclass=Singleton):
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        try:
            if subprocess.run([ffmpeg_path], capture_output=True).returncode != 1:
                raise FFmpegNotFoundError()
        except FileNotFoundError:
            raise FFmpegNotFoundError()

        self.path = os.path.normpath(ffmpeg_path)

    def exec(self, args: list[str]):
        cmd = [self.path]
        cmd.extend(args)
        Logger.debug(" ".join(cmd))
        # NOTE(aheadlead): FFmpeg 会谜之从 stdin 读取一个字节，这会让调用 yutto 的 shell 脚本踩到坑
        # 这个行为在目前最新的 FFmpeg 6.0 仍然存在
        return subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True)

    @cached_property
    def version(self) -> str:
        output = self.exec(["-version"]).stdout.decode()
        if match_obj := re.match(r"ffmpeg version (?P<version>(\S+)) Copyright", output):
            return match_obj.group("version")
        return "Unknown version"

    @cached_property
    def video_encodecs(self) -> list[str]:
        results: list[str] = []
        output = self.exec(["-codecs"]).stdout.decode()
        for line in output.split("\n"):
            if match_obj := re.match(r"^\s*[D\.]EV[I\.][L\.][S\.] (?P<vcodec>\S+)", line):
                results.append(match_obj.group("vcodec"))
        output = self.exec(["-encoders"]).stdout.decode()
        for line in output.split("\n"):
            if match_obj := re.match(r"^\s*V[F\.][S\.][X\.][B\.][D\.] (?P<encoder>\S+)", line):
                results.append(match_obj.group("encoder"))
        return results

    @cached_property
    def audio_encodecs(self) -> list[str]:
        results: list[str] = []
        output = self.exec(["-codecs"]).stdout.decode()
        for line in output.split("\n"):
            if match_obj := re.match(r"^\s*[D\.]EA[I\.][L\.][S\.] (?P<acodec>\S+)", line):
                results.append(match_obj.group("acodec"))
        output = self.exec(["-encoders"]).stdout.decode()
        for line in output.split("\n"):
            if match_obj := re.match(r"^\s*A[F\.][S\.][X\.][B\.][D\.] (?P<encoder>\S+)", line):
                results.append(match_obj.group("encoder"))
        return results
