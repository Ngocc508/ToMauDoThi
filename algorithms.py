import networkx as nx
import numpy as np

def tao_do_thi_ngau_nhien(n, p):
    """
    Tạo đồ thị ngẫu nhiên.
    Input: n (số đỉnh), p (xác suất nối).
    Output: Graph object, danh sách tên đỉnh, Ma trận kề.
    """
    # Tạo đồ thị ngẫu nhiên Erdos-Renyi
    G = nx.erdos_renyi_graph(n, p)
    
    # Đổi tên đỉnh từ 0,1,2 sang N0, N1, N2
    mapping = {i: f"N{i}" for i in range(n)}
    G = nx.relabel_nodes(G, mapping)
    
    nodes = list(G.nodes())
    # Chuyển sang ma trận kề dạng list
    matrix = nx.to_numpy_array(G).astype(int).tolist()
    
    return G, nodes, matrix

def giai_thuat_to_mau_ha_bac(nodes, G_matrix, palette):
    """
    Thuật toán tô màu theo lý thuyết:
    1. Chọn đỉnh bậc lớn nhất (trong các đỉnh chưa tô).
    2. Tô màu.
    3. Hạ bậc các đỉnh hàng xóm.
    """
    num_vertices = len(nodes)
    
    # Mapping tên đỉnh -> index
    t_ = {nodes[i]: i for i in range(num_vertices)}

    # Tính bậc ban đầu
    current_degrees = [sum(G_matrix[i]) for i in range(num_vertices)]
    
    colored_status = [False] * num_vertices # Đánh dấu đỉnh đã tô
    solution = {} # Lưu kết quả {Tên đỉnh: Màu}
    count_colored = 0

    # VÒNG LẶP CHÍNH
    while count_colored < num_vertices:
        
        # --- BƯỚC 1: Chọn đỉnh có bậc lớn nhất trong các đỉnh chưa tô ---
        max_degree = -1
        u_idx = -1
        
        for i in range(num_vertices):
            if not colored_status[i]:
                if current_degrees[i] > max_degree:
                    max_degree = current_degrees[i]
                    u_idx = i
        
        if u_idx == -1: break # Đã tô hết

        u_name = nodes[u_idx]

        # --- BƯỚC 2: Tô màu ---
        # Tìm các màu bị cấm (do hàng xóm đã tô)
        forbidden_colors = set()
        for v_idx in range(num_vertices):
            # Nếu là hàng xóm VÀ hàng xóm đã tô màu
            if G_matrix[u_idx][v_idx] == 1 and colored_status[v_idx]:
                neighbor_name = nodes[v_idx]
                forbidden_colors.add(solution[neighbor_name])
        
        # Chọn màu đầu tiên trong bảng màu không bị cấm
        assigned_color = 'gray' # Mặc định nếu thiếu màu
        for color in palette:
            if color not in forbidden_colors:
                assigned_color = color
                break
        
        solution[u_name] = assigned_color
        colored_status[u_idx] = True
        count_colored += 1

        # --- BƯỚC 3: Hạ bậc ---
        current_degrees[u_idx] = -1 

        for v_idx in range(num_vertices):
            if G_matrix[u_idx][v_idx] == 1 and not colored_status[v_idx]:
                current_degrees[v_idx] -= 1
                
    return solution