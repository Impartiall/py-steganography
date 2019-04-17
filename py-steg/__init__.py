from PIL import Image
import os


def encode(image, data=-1, output_file=None):
    imgdata = deconstruct(image)
    bindata = tobinary(imgdata["pixdata"])

    print(bindata)

    imgdata["pixdata"] = frombinary(bindata)
    new_img = reconstruct(imgdata)

    if output_file is None:
        output_file = "(altered) " + image
    new_img.save(generate_filepath(output_file))


# Watch out for jpeg compression issues!
def decode(image, output_file=None):
    pass


def generate_filepath(filename):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    return os.path.join(__location__, filename)


def tobinary(pixdata):
    return [tuple([bin(j) for j in triple]) for i, triple in enumerate(pixdata)]


def frombinary(bindata):
    return [tuple([int(j, 2) for j in triple]) for i, triple in enumerate(bindata)]


def deconstruct(imgpath):
    img = Image.open(generate_filepath(imgpath))

    return {"pixdata": img.getdata(), "imgsize": img.size}


def reconstruct(imgdata):
    img = Image.new("RGB", (imgdata["imgsize"]))
    img.putdata(imgdata["pixdata"])

    return img


encode("input_img.jpg")
