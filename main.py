#!/usr/bin/env python

import os
import sys

import cv2
import numpy as np

def jpeg_to_nv21(input_path):
    # Read the JPEG image
    img = cv2.imread(input_path)
    height, width, _ = img.shape
    output_path = os.path.splitext(input_path)[0] + f"_{width}_{height}_nv21.yuv"

    # Convert the color space from BGR (default in OpenCV) to YUV
    yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # Split YUV channels
    y, u, v = cv2.split(yuv_img)

    # Resize U and V channels to match Y channel dimensions
    u = cv2.resize(u, (y.shape[1] // 2, y.shape[0] // 2), interpolation=cv2.INTER_LINEAR)
    v = cv2.resize(v, (y.shape[1] // 2, y.shape[0] // 2), interpolation=cv2.INTER_LINEAR)

    # Interleave U and V channels to create NV21 format
    nv21_data = np.zeros((y.shape[0] * 3 // 2, y.shape[1]), dtype=np.uint8)
    nv21_data[:y.shape[0], :] = y
    nv21_data[y.shape[0]:, 0::2] = v
    nv21_data[y.shape[0]:, 1::2] = u

    # Save the NV21 raw data to a file
    with open(output_path, 'wb') as f:
        f.write(nv21_data.tobytes())


def main():
    if len(sys.argv) != 2:
        return

    input_image_path = sys.argv[1]

    jpeg_to_nv21(input_image_path)

    print("Conversion complete.")

if __name__ == "__main__":
    main()

