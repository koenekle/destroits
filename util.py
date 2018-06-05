#!/usr/bin/python
# -*- coding: <utf-8> -*-
import math

import numpy as np

Vector2D = np.ndarray(dtype=np.float64, shape=(2, 1))


def rotate(vector, degrees):
    a = np.radians(degrees)
    ca, sa = math.cos(a), math.sin(a)
    drehmatrix = np.array(
        [[ca, -sa],
         [sa, ca]])
    result = drehmatrix.dot(vector)
    return result


def cut_to_length(vector, length):
    return length * (vector / np.linalg.norm(vector))


def angle(vector_a, vector_b):
    if np.linalg.norm(vector_a) == 0 or np.linalg.norm(vector_b) == 0:
        return 0
    else:
        return (vector_a * vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
