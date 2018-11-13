import json

from config import (
    OUTFILE_PATH,
)


def write_data(data):
    with open(OUTFILE_PATH, 'w') as f:
        json.dump(data, f, default=lambda o: o.__dict__)

    print(f'Wrote post data to {OUTFILE_PATH}')
