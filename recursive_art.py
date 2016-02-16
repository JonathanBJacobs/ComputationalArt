""" Random art generator. Software Design Spring 2016

    @author: Jonathan B Jacobs
"""

import random
from PIL import Image
import math


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    functions = {1: "prod", 2: "avg", 3: "cos_pi", 4: "sin_pi",
                 5: "arctan", 6: "step", 7: "x", 8: "y"}

    depth = random.randint(min_depth, max_depth)
    funcNum = random.randint(1, 4)

    if depth != 0:
        if funcNum in [1, 2]:
            return [functions[funcNum],
                    build_random_function(depth-1, depth-1),
                    build_random_function(depth-1, depth-1)]
        else:
            return [functions[funcNum],
                    build_random_function(depth-1, depth-1)]
    else:
        return functions[random.randint(7, 8)]


def evaluate_random_function(f, x, y):

    """ Evaluate the random function f with input x
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    functions = {1: "prod", 2: "avg", 3: "cos_pi", 4: "sin_pi",
                 5: "arctan", 6: "step", 7: "x", 8: "y"}
    if len(f) == 3:
        eval1 = evaluate_random_function(f[1], x, y)
        eval2 = evaluate_random_function(f[2], x, y)
    elif len(f) == 2:
        eval1 = evaluate_random_function(f[1], x, y)

    if f[0] == functions[1]:
        return eval1 * eval2
    elif f[0] == functions[2]:
        return 0.5 * (eval1 + eval2)
    elif f[0] == functions[3]:
        return math.cos(math.pi * eval1)
    elif f[0] == functions[4]:
        return math.sin(math.pi * eval1)
    elif f[0] == functions[5]:
        return math.atan(eval1)/(math.pi)/2
    elif f[0] == functions[6]:
        if eval1 > 0:
            return 1
        elif eval1 == 0:
            return 0
        elif eval1 < 0:
            return -1
    elif f[0] == functions[7]:
        return x
    elif f[0] == functions[8]:
        return y


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    inputRange = 1.0*(input_interval_end - input_interval_start)
    outputRange = output_interval_end - output_interval_start
    val -= input_interval_start

    return val*outputRange/inputRange + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(11, 12)
    green_function = build_random_function(12, 13)
    blue_function = build_random_function(13, 14)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            print "i: " + str(i)
            print "j: " + str(j)
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("save4.png", 350, 350)
    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
