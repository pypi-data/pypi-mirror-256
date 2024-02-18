import os
from multiprocessing import Manager, Queue, Pool

import numpy as np
from PIL import Image

from patchify import unpatchify, patchify

from bpc.config import Config
from bpc.log import info, warn, time_log
from bpc.util import check_both_path_exists


class Convertor:
    def __init__(self, path: str, out_path: str, config: Config = Config()):
        self.path = path
        self.out_path = out_path
        self.config = config

    def multiple_convert(self):
        check_both_path_exists(self.path, self.out_path)

        for file in os.listdir(self.path):
            if not (file.endswith(".png") or file.endswith(".jpg")):
                continue

            self._convert(file, None)

    def single_convert(self, name: str, out_name: str = None, img_amount: int = 1):
        check_both_path_exists(self.path, self.out_path)

        for i in range(img_amount):
            self.config.MAX_RANGE = 10 if img_amount == 1 else 5 * (i + 1)
            self._convert(name, out_name)

    @time_log(far_from_utc=9)
    def _convert(self, name: str, out_name: str = None):
        info("Make image as array")
        Image.MAX_IMAGE_PIXELS = self.config.MAX_IMAGE_PIXEL
        image = Image.open(os.path.join(self.path, name)).convert("RGBA")
        image_array = np.asarray(image)
        height, width, channel_count = image_array.shape

        info("Create Patches")
        self._create_patches(image_array, channel_count)

        manager = Manager()
        que: Queue = manager.Queue()

        info("Create Patch list")
        patches_list = [
            [i, j, 0, que]
            for i in range(self.patches.shape[0])
            for j in range(self.patches.shape[1])
        ]

        info(f"Create Sub processes, i : {self.patches.shape[0]} j : {self.patches.shape[1]}")
        pool = Pool(self.config.CPU_AMOUNT)
        pool.starmap(self._sub_convert, patches_list)
        pool.close()
        pool.join()

        info("Organize Out Patches")
        self._organize_out_patches(que)

        info("Compress and Save Image")
        self._save_image_file(height, width, channel_count, name, out_name)

    def _sub_convert(self, i, j, l, que: Queue):
        patch = self.patches[i, j, l]
        data, should_change = self._check_should_change(patch)

        if should_change:
            out = self._change(data)

        else:
            out = patch

        que.put((i, j, l, out))

    def _create_patches(self, image_array, channel_count: int):
        self.patches = patchify(
            image_array,
            patch_size=(
                self.config.PATCH_HEIGHT,
                self.config.PATCH_WIDTH,
                channel_count
            ),
            step=self.config.STEP
        )
        self.output_patches = np.empty(self.patches.shape).astype(np.uint8)

    def _check_should_change(self, patch):
        p1 = np.array(patch)
        p1_size = (patch.shape[0], patch.shape[1])

        black_cnt = 0
        black_level = self.config.BLACK_PIXEL_LEVEL

        for row in range(p1_size[0]):
            for col in range(p1_size[1]):
                pixel = p1[row][col]

                r, g, b = pixel[0], pixel[1], pixel[2]

                if black_level >= r and black_level >= g and black_level >= b:
                    black_cnt += 1

                    if black_cnt > self.config.MAX_RANGE:
                        return p1, True

        return patch, False

    def _change(self, data):
        black_level = self.config.BLACK_PIXEL_LEVEL

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                pixel = data[i][j]

                if black_level >= pixel[0] and black_level >= pixel[1] and black_level >= pixel[2]:
                    data[i][j][3] = 0

        return data

    def _organize_out_patches(self, que):
        while not que.empty():
            i, j, l, data = que.get()

            self.output_patches[i, j, l] = data

    def _save_image_file(self, height, width, channel_count, name: str, out_name: str = None):
        if out_name is None:
            out_name = name.replace(".png", "_Pad_out.png")

        output_height = height - (height - self.config.PATCH_HEIGHT) % self.config.STEP
        output_width = width - (width - self.config.PATCH_WIDTH) % self.config.STEP
        output_shape = (output_height, output_width, channel_count)

        output_image = unpatchify(self.output_patches, output_shape)
        output_image = Image.fromarray(output_image)
        output_image.save(
            os.path.join(self.out_path, out_name),
            compress_level=self.config.COMPRESS_LEVEL,
            format="PNG"
        )
