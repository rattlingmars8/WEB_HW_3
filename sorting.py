from pathlib import Path
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import time

CATEGORIES = {
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'documents': ('.doc', '.docs', '.txt', '.pdf', '.xlsx', '.pptx'),
    'archives': ('.zip', '.gz', '.tar')
}


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def get_file_cat(file: str):
    full_file = Path(file)
    file_ext = full_file.suffix.lower()
    file_category = next((cat for cat, exts in CATEGORIES.items() if file_ext in exts), "OTHER")
    return file_category


def get_files(folder: Path):
    files = []
    items = folder.iterdir()
    with ThreadPoolExecutor() as executor:
        for item in items:
            if item.is_file():
                files.append(item)
            elif item.is_dir():
                future = executor.submit(get_files, item)
                files.extend(future.result())
    return files


def move_file(file, destination):
    try:
        shutil.move(file, destination)
        logger.info("Moved file %s to folder %s", file, destination)
    except shutil.Error:
        pass


def sort_folder(folder: Path):
    start_time = time.time()
    all_files = get_files(folder)
    other_folder = folder / "OTHER"
    other_folder.mkdir(exist_ok=True)

    sorted_files = True  # Флажок, який вказує, чи відсортовані файли.

    for category in CATEGORIES:
        root_category = folder / category
        root_category.mkdir(exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for file in all_files:
            destination = folder / get_file_cat(file)
            if destination != file.parent:  # Перевірка на те чи файл вже у папці призначення
                sorted_files = False
                executor.submit(move_file, file, destination)

    end_time = time.time()
    result_time = end_time - start_time
    logger.info("Total execution time: %.2f seconds", result_time)

    if sorted_files:
        logger.info("Nothing to sort. All files are already sorted.")


def del_empty(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            del_empty(item)
    if not any(folder.iterdir()):
        folder.rmdir()
        logger.info("Empty folder %s was removed.", folder.name)


def main():
    sort_folder(Path('C:/Users/Admin/Desktop/Хлам/'))
    del_empty(Path('C:/Users/Admin/Desktop/Хлам/'))


if __name__ == "__main__":
    main()
