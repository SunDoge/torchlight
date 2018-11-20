from collections.abc import Iterable
from abc import ABC, abstractmethod
import random


class Compose:

    def __init__(self, transforms):
        self.transforms = transforms

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string

    def __call__(self):
        options = {}
        for transform in self.transforms:
            transform.update(options)
        return options


# class Normalize:

#     def __init__(self, mean, std):
#         self.mean = mean
#         self.std = std

#     def

class NVVLTransform(ABC):

    @abstractmethod
    def update(self, options):
        pass


class Resize(NVVLTransform):
    def __init__(self, size, interpolation='Linear'):
        """
        Args:
            interpolation: ['Linear', 'Nearest']
        """
        assert isinstance(size, int) or (
            isinstance(size, Iterable) and len(size) == 2)

        if isinstance(size, int):
            self.scale_height = size
            self.scale_width = size
        else:
            self.scale_height = size[0]
            self.scale_width = size[1]

        self.scale_method = interpolation

    def update(self, options):
        # Scale won't resize the array. To remove the black area, we need to crop.
        self.options = {
            'scale_height': self.scale_height,
            'scale_width': self.scale_width,
            'scale_method': self.scale_method,
            'crop_height': self.scale_height,
            'crop_width': self.scale_width,
        }

        options.update(self.options)


class CenterCrop(NVVLTransform):
    def __init__(self, size, frame_size=None):
        if isinstance(size, int):
            self.crop_height = size
            self.crop_width = size
        else:
            self.crop_height = size[0]
            self.crop_width = size[1]

        self.frame_size = frame_size

    def update(self, options):
        if 'scale_height' not in options:
            assert self.frame_size is not None
            self.scale_height = self.frame_size[0]
            self.scale_width = self.frame_size[1]
        else:
            self.scale_height = options['scale_height']
            self.scale_width = options['scale_width']

        self.options = {
            'crop_heigth': self.crop_height,
            'crop_width': self.crop_width,
            'crop_x': (self.scale_height - self.crop_height) // 2,
            'crop_y': (self.scale_width - self.crop_width) // 2,
        }
        options.update(self.options)


class RandomHorizontalFlip(NVVLTransform):
    def __init__(self, p=0.5):
        self.p = p

    def update(self, options):
        if random.random() < self.p:
            self.horiz_flip = True
        else:
            self.horiz_flip = False

        options.update({'horiz_flip': self.horiz_flip})
