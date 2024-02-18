from dataclasses import dataclass
from os import cpu_count


@dataclass
class Config:
    CPU_AMOUNT: int

    MAX_RANGE: int
    COMMON_PARAM: int
    COMPRESS_LEVEL: int
    BLACK_PIXEL_LEVEL: int
    MAX_IMAGE_PIXEL: int

    PATCH_HEIGHT: int
    PATCH_WIDTH: int
    STEP: int

    def __init__(
            self,
            cpu_amount: int = cpu_count() - cpu_count() // 3,
            max_range: int = 10,
            common_param: int = 100,
            compress_level: int = 4,
            black_pixel_level: int = 0,
            max_image_pixels=933120000
    ):
        self.CPU_AMOUNT = cpu_amount
        self.MAX_RANGE = max_range
        self.MAX_IMAGE_PIXEL = max_image_pixels
        self.COMPRESS_LEVEL = compress_level
        self.BLACK_PIXEL_LEVEL = black_pixel_level

        self.COMMON_PARAM = common_param
        self.PATCH_HEIGHT, self.PATCH_WIDTH, self.STEP = common_param, common_param, common_param
