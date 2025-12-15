import networkx as nx # pyright: ignore[reportMissingModuleSource]
import numpy as np

def tao_do_thi_ngau_nhien(n, p):
    """
    Tạo đồ thị ngẫu nhiên Erdos-Renyi.
    Trả về: (graph_object, nodes_list, adjacency_matrix)
    """
    G = nx.erdos_renyi_graph(n, p)
    
    # Đổi tên đỉnh từ 0,1,2 sang N0, N1, N2
    mapping = {i: f"N{i}" for i in range(n)}
    G = nx.relabel_nodes(G, mapping)
    
    nodes = list(G.nodes())
    # Chuyển sang ma trận kề (list of lists) để thuật toán tô màu xử lý
    matrix = nx.to_numpy_array(G).astype(int).tolist()
    
    return G, nodes, matrix

def tao_do_thi_luoi(side):
    """
    Tạo đồ thị dạng lưới (Grid).
    Trả về: (graph_object, nodes_list, adjacency_matrix)
    """
    G = nx.grid_2d_graph(side, side)
    
    # Đổi tên đỉnh từ (0,1) sang string "0,1"
    mapping = {node: f"{node[0]},{node[1]}" for node in G.nodes()}
    G = nx.relabel_nodes(G, mapping)
    
    nodes = list(G.nodes())
    matrix = nx.to_numpy_array(G).astype(int).tolist()
    
    return G, nodes, matrix

def thuc_hien_to_mau(nodes, G_matrix, list_colors):
    """
    Thuật toán Greedy tô màu kết hợp lan truyền ràng buộc.
    Trả về: dictionary {Tên đỉnh: Tên màu}
    """
    n = len(nodes)
    t_ = {nodes[i]: i for i in range(n)} # Map tên đỉnh -> index

    # 1. Tính bậc của các đỉnh
    degree = [sum(G_matrix[i]) for i in range(n)]

    # 2. Khởi tạo miền giá trị (Domain) cho mỗi đỉnh
    colorDict = {node: list(list_colors) for node in nodes}

    # 3. Sắp xếp các đỉnh theo bậc giảm dần (Heuristic)
    indexed_degree = sorted([(i, degree[i]) for i in range(n)], key=lambda x: x[1], reverse=True)
    sortedNode = [nodes[x[0]] for x in indexed_degree]

    solution = {}

    # 4. Duyệt và tô màu
    for u in sortedNode:
        # Nếu không còn màu nào hợp lệ
        if not colorDict[u]:
            solution[u] = 'white' # Đánh dấu lỗi
            continue

        # Chọn màu đầu tiên hợp lệ (Greedy)
        chosen_color = colorDict[u][0]
        solution[u] = chosen_color

        # Lan truyền ràng buộc (Constraint Propagation)
        # Loại bỏ màu vừa chọn khỏi miền giá trị của các đỉnh kề
        u_idx = t_[u]
        for v_idx in range(n):
            if G_matrix[u_idx][v_idx] == 1: # Nếu kề nhau
                v_name = nodes[v_idx]
                if chosen_color in colorDict[v_name]:
                    colorDict[v_name].remove(chosen_color)
                    
    return solution