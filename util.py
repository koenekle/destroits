#!/usr/bin/python
# -*- coding: <utf-8> -*-
import math

import numpy as np

Vector2D = np.ndarray(dtype=np.float64, shape=(2, 1))


def rotate(vector: Vector2D, degrees: float):
    a = np.radians(degrees)
    ca, sa = math.cos(a), math.sin(a)
    drehmatrix = np.array(
        [[ca, -sa],
         [sa, ca]])
    result = drehmatrix.dot(vector)
    return result
