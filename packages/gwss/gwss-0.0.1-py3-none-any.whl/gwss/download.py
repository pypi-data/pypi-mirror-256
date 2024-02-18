import asyncio
import os
from pathlib import Path

import aiohttp
from gwss.logger import logger

async def download_file(url, package: str, name: str, version: str, ext: str, dest_dir: os.PathLike):
    """

    :param url:
    :param package: name of whole package
    :param name: name of package file
    :param version: version of package file
    :param ext: extension
    :param dest_dir: destination of files downloaded
    :return:
    """
    computed_filename = "%(name)s-%(version)s.%(ext)s".format(name, version, ext)
    assert Path(dest_dir).exists()

    dest_dir = Path(dest_dir)
    dest_file = Path.joinpath(dest_dir,computed_filename )
    logger.debug("Downloading file %(computed_filename)s to %(dest_file)s")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "content-disposition" in response.headers:
                header = response.headers["content-disposition"]
                file = header.split("filename=")[1]
            else:
                file = url.split("/")[-1]
            with open(file, mode="wb") as file:
                while True:
                    chunk = await response.content.read()
                    if not chunk:
                        break
                    file.write(chunk)
                print(f"Downloaded file {file}")