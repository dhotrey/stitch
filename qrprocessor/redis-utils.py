import redis
import base64
import hashlib


def ReadChunkData() -> list:
    rdb = redis.Redis()
    chunk_data = rdb.lrange("chunkdata", 0, -1)
    decoded_data = [base64.b64decode(i) for i in chunk_data]

    for idx, d in enumerate(decoded_data):
        sha256 = hashlib.sha256(d).hexdigest()
        print(f"sha256 for {idx} -> {sha256}")

    return decoded_data


