import open3d as o3d
import numpy as np
import math
            
class EgoCar:
    def __init__(self):
        vertices = np.array([
            # 底面 (z=0)
            [-0.5, -0.5, 0.0],  # v0
            [ 0.5, -0.5, 0.0],  # v1
            [ 0.5,  0.5, 0.0],  # v2
            [ 0.0,  1.0, 0.0],  # v3 (三角形の頂点)
            [-0.5,  0.5, 0.0],  # v4    
            # 上面 (z=1)
            [-0.5, -0.5, 0.8],  # v5
            [ 0.5, -0.5, 0.8],  # v6
            [ 0.5,  0.5, 0.8],  # v7
            [ 0.0,  1.0, 0.8],  # v8 (三角形の頂点)
            [-0.5,  0.5, 0.8]   # v9
        ])
        
        # 面 (Triangles) の定義
        # すべての法線が外側を向くように頂点の巻順を統一
        triangles = np.array([
            # 底面 (法線が下向き: -Z方向)
            [0, 2, 1], [0, 4, 2], [2, 4, 3],
            # 上面 (法線が上向き: +Z方向) - ★修正点
            [5, 6, 7], [5, 7, 9], [7, 8, 9],
            # 側面 (法線が外向き) - ★修正点
            [0, 1, 6], [0, 6, 5],  # 側面 1
            [1, 2, 7], [1, 7, 6],  # 側面 2
            [2, 3, 8], [2, 8, 7],  # 側面 3
            [3, 4, 9], [3, 9, 8],  # 側面 4
            [4, 0, 5], [4, 5, 9]   # 側面 5
        ])
        self.mesh = o3d.geometry.TriangleMesh()
        self.mesh.vertices = o3d.utility.Vector3dVector(vertices)
        self.mesh.triangles = o3d.utility.Vector3iVector(triangles)

        self.mesh.compute_vertex_normals()
        self.mesh.paint_uniform_color([1.0, 0.0, 0.0])
        
        # position and
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.yaw = 90.0
    
    def move(self, distance):
        yaw_rad = math.radians(self.yaw)
        dx = distance * math.cos(yaw_rad)
        dy = distance * math.sin(yaw_rad)
        self.mesh.translate((dx, dy, 0), relative=True)
        self.x += dx
        self.y += dy

        print(self.x, self.y, self.yaw)

    def rotate(self, dyaw):
        yaw_rad = math.radians(dyaw)
        rotation_matrix = o3d.geometry.get_rotation_matrix_from_axis_angle([0, 0,yaw_rad])
        self.mesh.rotate(rotation_matrix, center=(self.x, self.y, 0))
        self.yaw += dyaw



ego_car = EgoCar()
distance = 0.2
dyaw = 5.0

vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()
vis.add_geometry(ego_car.mesh)

pcd_map = o3d.io.read_point_cloud("/Users/tsunogayashouta/Downloads/MapViewer3Dpts_out.xyz")
vis.add_geometry(pcd_map)

view_control = vis.get_view_control()
# view_control.set_zoom(10)

def move_forward(vis):
    print("Move forward (W)")
    ego_car.move(distance)
    vis.update_geometry(ego_car.mesh)

def move_backward(vis):
    print("Move forward (S)")
    ego_car.move(-1 * distance)
    vis.update_geometry(ego_car.mesh)

def rotate_left(vis):
    print("Rotate left (Q)")
    ego_car.rotate(dyaw)
    vis.update_geometry(ego_car.mesh)

def rotate_right(vis):
    print("Rotate right (E)")
    ego_car.rotate(-1 * dyaw)
    vis.update_geometry(ego_car.mesh)

vis.register_key_callback(ord("W"), move_forward)
vis.register_key_callback(ord("S"), move_backward)
vis.register_key_callback(ord("A"), rotate_left)
vis.register_key_callback(ord("D"), rotate_right)

def update_view(vis):
    vis.poll_events()
    vis.update_renderer()

vis.run()
vis.destroy_window()