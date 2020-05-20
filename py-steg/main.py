from PIL import Image
import binascii
import fire


def encode(image, data, output_file="altered_image.png", encryption=None):
    imgdata = deconstruct(image)
    bindata = pix_tobinary(imgdata["pixdata"])

    binstr = file_tobinary(data)[2:]
    if len(binstr) > len(bindata) * 3:
        raise Exception("File being encoded is too large!")

    binstr = binstr.zfill(len(bindata) * 3)

    bindata = [
        tuple([val[:-1] + binstr[(i * 3) + j] for j, val in enumerate(triple)])
        for i, triple in enumerate(bindata)
    ]

    imgdata["pixdata"] = pix_frombinary(bindata)
    new_img = reconstruct(imgdata)

    if output_file.split(".")[-1] in ["jpg", "gif"]:
        raise Exception("Do not use lossy file formats!")

    new_img.save(output_file)


def decode(image, output_file="hidden_file.txt"):
    imgdata = deconstruct(image)
    bindata = pix_tobinary(imgdata["pixdata"])

    binstr = ""
    for i in range(len(bindata)):
        for j in range(3):
            binstr += bindata[i][j][-1]

    file_frombinary(binstr, output_file)


def file_tobinary(filename):
    with open(filename, "rb") as f:
        bindata = f.read()

    hexdata = binascii.hexlify(bindata)
    return bin(int(hexdata, 16))


def file_frombinary(binstr, filename):
    hexdata = hex(int(binstr.replace("0b", ""), 2))
    bindata = binascii.unhexlify(hexdata.strip("0x"))

    with open(filename, "wb") as f:
        f.write(bindata)


def pix_tobinary(pixdata):
    return [tuple([bin(j) for j in triple]) for i, triple in enumerate(pixdata)]


def pix_frombinary(bindata):
    return [tuple([int(j, 2) for j in triple]) for i, triple in enumerate(bindata)]


def deconstruct(imgpath):
    img = Image.open(imgpath)

    return {"pixdata": img.getdata(), "imgsize": img.size}


def reconstruct(imgdata):
    img = Image.new("RGB", (imgdata["imgsize"]))
    img.putdata(imgdata["pixdata"])

    return img


if __name__ == "__main__":
    fire.Fire({"encode": encode, "decode": decode})
