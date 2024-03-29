import bz2
import io
import sqlite3

import pandas as pd
import requests

from core import config

conn = sqlite3.connect(config.DATABASE_PATH)
c = conn.cursor()


def download_csv() -> bytes:
    """Download the BZ2 compressed invTypes.csv file located at
    https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2 and
    return the content as a bytestring
    """

    response = requests.get('https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2')
    response.raise_for_status()
    return response.content


def decompress_csv(csv_bytes):
    return io.BytesIO(bz2.decompress(csv_bytes))


def write_types(types):
    for type_id, name in types:
        c.execute("INSERT INTO items VALUES (?,?,0,0);", (type_id, name))
    conn.commit()


def main():
    compressed_csv = download_csv()
    csv = decompress_csv(compressed_csv)
    df = pd.read_csv(csv)
    types = zip(df.typeID, df.typeName)
    write_types(types)


if __name__ == '__main__':
    main()
    c.close()
    conn.close()
