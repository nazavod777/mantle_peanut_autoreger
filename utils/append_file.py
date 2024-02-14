import aiofiles


async def append_file(file_folder: str,
                      file_text: str) -> None:
    async with aiofiles.open(file=file_folder,
                             mode='a',
                             encoding='utf-8-sig') as file:
        await file.write(file_text)
