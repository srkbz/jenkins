import requests
from tqdm import tqdm


def download_file(url: str, destination: str, description: str, chunk_size: int = 1024):
    resp = requests.get(url, allow_redirects=True, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(destination, "wb") as file, tqdm(
        desc=description,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
