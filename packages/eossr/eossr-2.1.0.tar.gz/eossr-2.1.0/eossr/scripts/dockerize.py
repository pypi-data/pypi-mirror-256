from eossr.api.ossr import get_ossr_records
from urllib.request import urlopen
from eossr.utils import ZipUrl
from pathlib import Path
import os
import shutil
import zipfile



def get_dockerfile_from_zipurl(url, **zipurl_kwargs):
    """
    Extract and reads codemeta metadata from a zip url.
    A codemeta.json file must be present in the zip archive.

    Parameters
    ----------
    url: string
        url to a zip file
    zipurl_kwargs: dictionnary
        metadata in the codemeta.json file in the zip archive

    Returns
    -------
    dict
    """
    zipurl_kwargs.setdefault('initial_buffer_size', 100)
    zipurl = ZipUrl(url, **zipurl_kwargs)

    dockerfiles = zipurl.find_files('Dockerfile')
    # if there are more than one Dockerfile file in the archive, we consider the one in the root directory, hence the
    # one with the shortest path
    dockerfile = min(dockerfiles, key=len)
    recipe = zipurl.read(dockerfile).decode('utf-8')
    return recipe


def get_dockerfile(record):
    """
    Get Dockerfile from the record (can also be in a zip archive).
    Raises an error if no `Dockerfile` is found.

    Parameters
    ----------
    zipurl_kwargs : dict
        kwargs for `eossr.utils.ZipUrl`

    Returns
    -------
    str
        Dockerfile content
    Raises
    ------
    FileNotFoundError
        If no `Dockerfile` is found in the record.
    """
    if 'files' not in record.data:
        raise FileNotFoundError(
            f'The record {record.id} does not contain any file')

    dockerfile_paths = [s for s in record.filelist if 'Dockerfile' in Path(
        s.rsplit('/content', maxsplit=1)[0]).name]
    ziparchives = [s for s in record.filelist if s.endswith('.zip/content')]
    if len(dockerfile_paths) >= 1:
        # if there are more than one Dockerfile in the repository, we consider the one in the root directory,
        # hence the one with the shortest path
        chosen_dockerfile = min(dockerfile_paths, key=len)
        return urlopen(chosen_dockerfile).read().decode('utf-8')
    elif len(ziparchives) > 0:
        for zipurl in ziparchives:
            try:
                return get_dockerfile_from_zipurl(zipurl)
            except FileNotFoundError:
                pass
        raise FileNotFoundError(
            f"No `Dockerfile` found in record {record.id}")
    else:
        raise FileNotFoundError(
            f"No `Dockerfile` found in record {record.id}")



def unzip_all(directory='.'):
    """
    Unzip zip files in a directory.

    Parameters
    ----------
    directory : str, optional
        Directory path to unzip files in, by default '.' (current directory)
    """
    for file in os.listdir(directory):
        if file.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(directory, file), 'r') as zip_ref:
                zip_ref.extractall(directory)


if __name__ == "__main__":
    records = get_ossr_records(size=4)
    records_with_dockerfile = []
    dockerfiles = {}

    for record in records:
        if len(records_with_dockerfile) > 1:
            break
        try:
            dockerfile = get_dockerfile(record)
            records_with_dockerfile.append(record.id)
            # record.download(f"record_{record.id}")
        except FileNotFoundError:
            pass

    for record_id in records_with_dockerfile:
        print(record_id)
        os.chdir(f"record_{record_id}")
        unzip_all()
        dockerfiles[record_id] = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == 'Dockerfile':
                    dockerfiles[record_id].append(os.path.join(root, file))

        if dockerfiles[record_id]:
            dockerfiles[record_id] = Path(f"record_{record_id}", min(dockerfiles[record_id], key=len))

        os.chdir('..')

    print(dockerfiles)
