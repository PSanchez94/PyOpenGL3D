# coding=utf-8
"""
Pablo Sanchez
CC3501 - 2020-2

Monkey Jump 3D:
A Python OpenGL 3D implementation of a platform game.
"""

import math
import glfw
from OpenGL.GL import *
import sys
import csv
import numpy as np

import include.transformations as tr
import include.basic_shapes as bs
import include.easy_shaders as es

import controller

controller = controller.Controller()


def createPlane(axis, x, y, texture):
    vertices = None

    # Defining the location and colors of each vertex  of the shape
    if axis == "z":
        vertices = [
            #    positions        colors
            0.0, 0.0, 0.0, 0.0, 1.0,
            x, 0.0, 0.0, 1.0, 1.0,
            x, y, 0.0, 1.0, 0.0,
            0.0, y, 0.0, 0.0, 0.0]

    elif axis == "x":
        vertices = [
            #    positions        colors
            0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, 0.0, y, 0.0, 0.0,
            x, 0, y, 1.0, 0.0,
            x, 0, 0, 1.0, 1.0]

    elif axis == "y":
        vertices = [
            #    positions        colors
            0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, x, 0.0, 1.0, 1.0,
            0.0, x, y, 1.0, 0.0,
            0.0, 0.0, y, 0.0, 0.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return bs.Shape(vertices, indices, texture)


def createHeartQuad():

    # Defining locations and colors for each vertex of the shape
    vertices = [
    #   positions        colors
        0.0, 0.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 0.0, 1.0, 0.0,
        0.0, 1.0, 0.0, 0.0, 0.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return bs.Shape(vertices, indices, "texture/heart.png")


def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_A:
            controller.leftKeyOn = True
        elif key == glfw.KEY_D:
            controller.rightKeyOn = True
        elif key == glfw.KEY_W:
            controller.backwrdKeyOn = True
        elif key == glfw.KEY_S:
            controller.forwrdKeyOn = True
        elif key == glfw.KEY_SPACE and not controller.jumpKeyOn:
            controller.jumpKeyOn = True
        elif key == glfw.KEY_X:
            controller.fillPolygon = not controller.fillPolygon
        elif key == glfw.KEY_ESCAPE:
            sys.exit()

    elif action == glfw.RELEASE:
        if key == glfw.KEY_A:
            controller.leftKeyOn = False
        elif key == glfw.KEY_D:
            controller.rightKeyOn = False
        if key == glfw.KEY_W:
            controller.backwrdKeyOn = False
        elif key == glfw.KEY_S:
            controller.forwrdKeyOn = False
        elif key == glfw.KEY_SPACE and controller.jumpKeyOn:
            controller.jumpKeyOn = False


if __name__ == "__main__":

    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0.0
        depth = 0.0
        for row in csv_reader:
            for i in range(5):
                if row[i] == "1":
                    controller.add_platform(4 - i, round(depth, 1), line_count)
                elif row[i] == "x":
                    controller.add_fake_platform(4 - i, round(depth, 1), line_count)
            line_count += 1
            depth = 1 - np.cos(np.pi * 0.5 * line_count)

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
    mj_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    ui_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory

    # Health GPUShape
    gpuHeartQuad = es.toGPUShape(createHeartQuad(), GL_REPEAT, GL_LINEAR)

    # Creating the main world planes
    gpuFloorPlane = es.toGPUShape(createPlane("z", 9, 9, "texture/grass.png"), GL_REPEAT, GL_LINEAR)
    gpuBackPlane = es.toGPUShape(createPlane("x", 9, 4*9, "texture/skyfullside.png"), GL_REPEAT, GL_LINEAR)
    gpuSidePlane = es.toGPUShape(createPlane("y", 9, 4*9, "texture/skyfullside.png"), GL_REPEAT, GL_LINEAR)

    scene_movement = 1.0
    scene_moving = False
    scene_up_view = False
    monkey_right = False
    monkey_left = False
    ortho_view = False

    # Creating monkey and banan and their GPUShapes
    controller.createMonkey()
    controller.monkey.createShape(
        es.toGPUShape(controller.monkey.hitboxShape("texture/monkey.png"), GL_REPEAT, GL_LINEAR))
    controller.createBanana()
    controller.banana.createShape(
        es.toGPUShape(controller.banana.hitboxShape("texture/bananacrate.png"), GL_REPEAT, GL_LINEAR))

    # Creating platform and bullet GPUShapes
    platform_gpuShape = None
    bullet_gpuShape = None
    for platform in controller.platform_list:
        if platform_gpuShape is None:
            platform_gpuShape = es.toGPUShape(
                platform.hitboxShape("texture/platform3d.png"), GL_REPEAT, GL_LINEAR)
        platform.createShape(platform_gpuShape)

    for fake_platform in controller.fake_platform_list:
        if platform_gpuShape is None:
            platform_gpuShape = es.toGPUShape(
                platform.hitboxShape("texture/platform3d.png"), GL_REPEAT, GL_LINEAR)
        fake_platform.createShape(platform_gpuShape)

    # Using perspective projection
    projection = tr.perspective(50, float(width) / float(height), 0.1, 100)

    # Main angled view
    side_view = np.array([5 * np.cos(np.pi / 4), 10 * np.cos(np.pi / 4), 2])
    viewPos = side_view

    t0 = glfw.get_time()
    controller.t1 = t0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        controller.t1 = t1

        if glfw.get_key(window, glfw.KEY_B) == glfw.PRESS:
            scene_up_view = False
            viewPos = side_view

        elif glfw.get_key(window, glfw.KEY_N) == glfw.PRESS:
            scene_up_view = False
            viewPos = np.array([0, 8, 0.1])

        elif glfw.get_key(window, glfw.KEY_M) == glfw.PRESS:
            scene_up_view = True
            viewPos = np.array([0, 0.1, 7])

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        ## 3D shader program
        glUseProgram(mj_pipeline.shaderProgram)

        # Define perspective projection
        glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "projection"),
                           1, GL_TRUE, projection)

        # Define camera view
        glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "view"),
                           1, GL_TRUE, view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Drawing Planes
        glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"),
                           1, GL_TRUE, tr.translate(-3.5, -2.0, -scene_movement))
        mj_pipeline.drawShape(gpuFloorPlane)
        mj_pipeline.drawShape(gpuBackPlane)
        mj_pipeline.drawShape(gpuSidePlane)

        # Drawing Monkey
        glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"), 1, GL_TRUE,
                           tr.translate(controller.monkey.x - 3.5,
                                        controller.monkey.y - 1.5,
                                        controller.monkey.z - scene_movement))
        mj_pipeline.drawShape(controller.monkey.hitbox_shape)

        # Drawing Platforms
        for platform in controller.platform_list:
            glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"),
                               1, GL_TRUE, tr.translate(platform.x - 3.5,
                                                        platform.y - 1.5,
                                                        platform.z - scene_movement))

            if scene_up_view and -3 < platform.z - controller.monkey.z < 1.0:
                mj_pipeline.drawShape(platform.hitbox_shape)
            elif not scene_up_view:
                mj_pipeline.drawShape(platform.hitbox_shape)

        # Drawing Fake Platforms
        for fake_platform in controller.fake_platform_list:
            glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"),
                               1, GL_TRUE, tr.translate(fake_platform.x - 3.5,
                                                        fake_platform.y - 1.5,
                                                        fake_platform.z - scene_movement))

            if np.sin((fake_platform.blink_time - t1)*np.pi*5) < 0 and fake_platform.blinking:
                mj_pipeline.drawShape(fake_platform.hitbox_shape)
            elif not fake_platform.blinking:
                if scene_up_view and -3 < fake_platform.z - controller.monkey.z < 1.0:
                    mj_pipeline.drawShape(fake_platform.hitbox_shape)
                elif not scene_up_view:
                    mj_pipeline.drawShape(fake_platform.hitbox_shape)

        ## Game mechanics within iteration

        # Move scene upon reaching 2 floors above current one
        if math.floor(controller.monkey.z) > controller.current_floor + 1.0 and scene_moving is False:
            scene_moving = True
            controller.current_floor = math.floor(controller.monkey.z)

        # Move the scene smoothly
        if scene_moving and scene_movement < controller.current_floor:
            scene_movement += 0.05
            if scene_movement > controller.current_floor:
                scene_moving = False

        # Lose condition upon reaching base of scene
        if (controller.monkey.z < scene_movement - 2.3 or
                controller.monkey.hitpoints == 0) and controller.lost is False:
            controller.monkey.hitpoints = 0
            controller.lost = True
            controller.end_game_time = t1

        # Jump is key has been pressed and monkey is airborne
        if controller.jumpKeyOn and controller.monkey.is_falling is False:
            controller.monkey.start_jump()

        # Bullets iteration
        controller.check_bullets(t1)

        # Drawing Bullets
        for a_bullet in controller.bullets:
            if bullet_gpuShape is None:
                bullet_gpuShape = es.toGPUShape(
                    a_bullet.hitboxShape("texture/bullet.png"), GL_REPEAT, GL_LINEAR)
            if a_bullet.hitbox_shape is None:
                a_bullet.createShape(bullet_gpuShape)

            bullet_translate = tr.translate(a_bullet.x - 3.5,
                                            a_bullet.y - 1.5,
                                            a_bullet.z - scene_movement)
            if a_bullet.speed < 0.0:
                glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
                                   bullet_translate,
                                   tr.rotationZ(np.pi),
                                   tr.translate(-a_bullet.width*0.5,
                                                -a_bullet.depth*0.5,
                                                -a_bullet.height*0.5)]))
            else:
                glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"),
                                   1, GL_TRUE, bullet_translate)
            mj_pipeline.drawShape(a_bullet.hitbox_shape)

        banana_translates = [
            tr.translate(controller.banana.x - 3.5,
                         controller.banana.y - 1.5,
                         controller.banana.z - scene_movement),
            tr.translate(- controller.banana.width*0.5,
                         - controller.banana.depth*0.5,
                         - controller.banana.height*0.5),
            tr.rotationZ(t1 * 2)]

        # Win condition
        if controller.won is False and controller.monkey.has_banana:
            controller.won = True
            controller.end_game_time = t1
        elif controller.won:
            monkey_left = False
            monkey_right = False
            controller.leftKeyOn = False
            controller.rightKeyOn = False

            glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
                banana_translates[0],
                tr.uniformScale(np.sin(t1 * 10) * 0.5 + 1.5),
                banana_translates[2],
                banana_translates[1]]))
            mj_pipeline.drawShape(controller.banana.hitbox_shape)

            if t1 - controller.end_game_time > 2.0:
                sys.exit("You won!")
        else:
            glUniformMatrix4fv(glGetUniformLocation(mj_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
                banana_translates[0],
                tr.uniformScale(np.sin(t1 * 3) * 0.5 + 1.5),
                banana_translates[2],
                banana_translates[1]]))
            mj_pipeline.drawShape(controller.banana.hitbox_shape)
            controller.moveMonkey()


        # Lose animation start and end
        if controller.lost:
            monkey_left = False
            monkey_right = False
            controller.monkey.collision = False
            controller.monkey.start_jump()
            controller.monkey.is_falling = False
            controller.leftKeyOn = False
            controller.rightKeyOn = False
            if t1 - controller.end_game_time > 1:
                if controller.monkey.hitpoints == 0:
                    sys.exit("You died.")
                else:
                    sys.exit("You fell out.")

        ## UI 2D shader program
        glUseProgram(ui_pipeline.shaderProgram)

        # Draw health UI
        for i in range(controller.monkey.hitpoints):
            glUniformMatrix4fv(glGetUniformLocation(ui_pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.scale(0.1, 0.1, 1.0),
                tr.translate(-4.0 - (3-i)*1.5, -9.0, 0)]))
            ui_pipeline.drawShape(gpuHeartQuad)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
