import pynvvl
from torch.utils.data import Dataset
from torch.utils.dlpack import from_dlpack


class Loader:

    def __init__(self, device_id=0, frame=0, count=None, transform=None, log_level='warn'):
        self.transform = transform if transform else {}
        self.device_id = device_id
        self.log_level = log_level
        self.frame = frame
        self.count = count
        self.loader = pynvvl.NVVLVideoLoader(device_id, log_level)

    def read_sequence(self, filename):
        options = {
            'frame': self.frame,
            'count': self.count
        }
        options.update(self.transform())
        video = self.loader.read_sequence(filename, options)
        tensor = from_dlpack(video.toDlpack())
        return tensor


if __name__ == '__main__':
    import transforms
    import torch

    data_transform = transforms.Compose([
        transforms.Resize(256)
    ])
    loader = Loader(transform=data_transform)
    video = loader.read_sequence('/home/sundoge/Videos/sim_00000.mp4')
    print(video.shape)
