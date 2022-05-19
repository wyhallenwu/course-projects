from Crypto.Hash import SHA256

chunk_size = 1024


def hash_video(filename):
    segment = []

    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if len(data) == 0:
                break
            segment.append(data)
    segment.reverse()
    result = 0
    for i, seg in enumerate(segment):
        if i < len(segment) - 1:
            segment[i + 1] += SHA256.new(seg).digest()
        else:
            result = SHA256.new(seg).hexdigest()
    return result


if __name__ == '__main__':
    valid_example = hash_video("./videos/6.2.birthday.mp4_download")
    print(valid_example)
    valid_result = '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'
    print(valid_example == valid_result)
    test_result = hash_video("./videos/6.1.intro.mp4_download")
    print(test_result)
