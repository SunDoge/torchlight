from torchlight.video import transforms


def test_compose():
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
    ])
    print(transform())
