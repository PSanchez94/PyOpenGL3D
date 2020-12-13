# coding=utf-8
"""
Pablo Sanchez
CC3501 - 2020-2

Monkey Jump 3D:
A Python OpenGL 3D implementation of a platform game.
"""

import glfw
from OpenGL.GL import *
import sys
import csv
import numpy as np

import include.transformations as tr
import include.basic_shapes as bs
import include.scene_graph as sg
import include.easy_shaders as es


import controller

controller = controller.Controller()


def createPlane(length, r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        0, 0,  0, r, g, b,
        length, 0,  0, r, g, b,
        length,  length,  0, r, g, b,
        0,  length,  0, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return bs.Shape(vertices, indices)


def on_key(window, key, scancode, action, mods):

    if action == glfw.PRESS:
        if key == glfw.KEY_A:
            controller.leftKeyOn = True
        elif key == glfw.KEY_D:
            controller.rightKeyOn = True
        elif key == glfw.KEY_W and not controller.jumpKeyOn:
            controller.jumpKeyOn = True
        elif key == glfw.KEY_ESCAPE:
            sys.exit()

    elif action == glfw.RELEASE:
        if key == glfw.KEY_A:
            controller.leftKeyOn = False
        elif key == glfw.KEY_D:
            controller.rightKeyOn = False
        elif key == glfw.KEY_W and controller.jumpKeyOn:
            controller.jumpKeyOn = False


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Monkey Jump 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    gpuZPlane = es.toGPUShape(createPlane(7, 0.3, 0.9, 0))

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    side_view = np.array([10 * np.cos(np.pi / 4), 10 * np.cos(np.pi / 4), 6])
    viewPos = side_view

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_B) == glfw.PRESS:
            viewPos = side_view

        elif glfw.get_key(window, glfw.KEY_N) == glfw.PRESS:
            viewPos = np.array([0, 10, 0.1])

        elif glfw.get_key(window, glfw.KEY_M) == glfw.PRESS:
            viewPos = np.array([0, 0.1, 10])

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"),
                           1,
                           GL_TRUE,
                           view)

        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"),
                           1,
                           GL_TRUE,
                           tr.translate(-3.5, 0, 0))
        mvpPipeline.drawShape(gpuZPlane)



        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"),
                               1,
                               GL_TRUE,
                               tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"),
                               1,
                               GL_TRUE,
                               tr.translate(-3.5, -3.5, 0))
            mvpPipeline.drawShape(gpuZPlane)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
