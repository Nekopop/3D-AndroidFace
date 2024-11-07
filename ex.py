import numpy as np
import trimesh
import os
from scipy.spatial.transform import Rotation as R

def align_model(mesh, model_points, reference_points):
    try:
        # モデルポイントと基準ポイントをnumpy配列に変換
        model_points = np.array(model_points, dtype=np.float32)
        reference_points = np.array(reference_points, dtype=np.float32)
        
        print("Model Points:", model_points)
        print("Reference Points:", reference_points)
        
        # モデルポイントの重心を計算
        model_center = np.mean(model_points, axis=0)
        reference_center = np.mean(reference_points, axis=0)
        
        print("Model Center:", model_center)
        print("Reference Center:", reference_center)
        
        # モデルポイントと基準ポイントを重心に合わせて平行移動
        model_points_centered = model_points - model_center
        reference_points_centered = reference_points - reference_center
        
        print("Model Points Centered:", model_points_centered)
        print("Reference Points Centered:", reference_points_centered)
        
        # SVDを使用して回転行列を計算
        H = model_points_centered.T @ reference_points_centered
        U, S, Vt = np.linalg.svd(H)
        R_matrix = Vt.T @ U.T
        
        print("Rotation Matrix:", R_matrix)
        
        # 回転行列をメッシュの頂点に適用
        vertices = np.array(mesh.vertices)
        vertices_centered = vertices - model_center
        transformed_vertices = vertices_centered @ R_matrix.T + reference_center
        
        # 正規化後のモデルポイントを計算
        normalized_model_points = model_points_centered @ R_matrix.T + reference_center
        print("Normalized Model Points:", normalized_model_points)
        
        # 正規化されたメッシュを作成
        normalized_mesh = trimesh.Trimesh(vertices=transformed_vertices, faces=mesh.faces)
        return normalized_mesh
    except Exception as e:
        print(f"Error in align_model: {e}")
        return None

# 基準座標系の4点を定義
reference_points = [
    [-37.54, 47.645, 33.984],   # 標準の右
    [-11.335, 60.624, -72.971], # 標準の上
    [33.808, -34.263, -46.805], # 標準の左
    [-66.826, -9.3204, 52.462]          # 追加の基準点，右耳裏
]

# 更新された各状態のくぼみの座標リスト
model_points_list = [
    [[-46.85, -49.644, -7.6998], [-75.008, 52.31, -37.27], [21.507, 65.869, -8.0156], [12.152, -74.244, -24.869]],     # 左下瞼0
    [[-24.833, -54.395, -30.895], [-84.395, 36.422, -41.933], [-4.8322, 65.769, 25.825], [41.638, -53.815, -39.189]],  # 左下瞼188
    [[-32.781, -55.157, -25.999], [-82.695, 41.448, -43.82], [0.071894, 68.252, 19.47], [32.43,-60.504, -36.146]],   # 上瞼左204
    [[14.649, 66.162, 7.0221], [4.1105, 32.412, -97.898], [-1.5172, -58.904, -40.511], [-30.39, 46.522, 52.298]],    # 眉寄せ255
    [[-48.905, -46.263, -16.128], [-75.795, 59.401, -30.95], [20.718, 64.826, 18.684], [11.299, -68.619, -35.47]],    # 頬引き右左191口引き255
    [[-48.776, -45.821, -10.698], [-77.101, 56.431, -37.344], [19.279, 68.545, 9.262], [9.6138, -69.822, -28.626]]     # 頬引き右左191
]

# OBJファイルのリスト
obj_files = ["hidarisitamabuta0.obj", "hidarisitamabuta188.obj", "uemabutahidari204.obj", "mayuyose255.obj", "hohohidarimigi191kutihiki255.obj", "hohohikimigihidari191.obj"]
output_folder = "normalized_models"  # 保存先のフォルダ

# 保存先フォルダを作成
os.makedirs(output_folder, exist_ok=True)

# 各モデルに対して正規化処理を適用
for obj_file, model_points in zip(obj_files, model_points_list):
    print(f"Processing {obj_file}...")
    try:
        # OBJファイルを読み込み
        mesh = trimesh.load(obj_file)
        print(f"Loaded {obj_file}")
        
        # 基準座標系に正規化
        normalized_mesh = align_model(mesh, model_points, reference_points)
        if normalized_mesh is not None:
            # 正規化後のモデルを保存
            output_path = os.path.join(output_folder, os.path.basename(obj_file))
            normalized_mesh.export(output_path)
            print(f"Normalized {obj_file} and saved to {output_path}")
        else:
            print(f"Failed to normalize {obj_file}.")
    except Exception as e:
        print(f"Error processing {obj_file}: {e}")
