# shader.py
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main() {
    FragColor = vec4(1.0);  // White color
}
"""
