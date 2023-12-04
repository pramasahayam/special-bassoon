# rocket.py
import numpy as np
import OpenGL.GL as gl

class Rocket:
    def __init__(self, obj_file_path):
        self.vertices = self.load_obj(obj_file_path)
        self.vertex_count = len(self.vertices)
        self.vertices = np.array(self.vertices, dtype=np.float32).flatten()

        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices, gl.GL_STATIC_DRAW)

    def load_obj(self, file_path):
        vertices = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vertex data
                    _, x, y, z = line.split()
                    vertices.append([float(x), float(y), float(z)])
        return vertices

    def render(self):
        gl.glEnableVertexAttribArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 0, None)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertex_count)
        gl.glDisableVertexAttribArray(0)
