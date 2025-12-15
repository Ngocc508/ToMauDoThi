import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx # pyright: ignore[reportMissingModuleSource]

# --- IMPORT MODULE CỦA CHÚNG TA ---
import algorithms as algo 

class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring - Constraint Satisfaction Problem")
        self.root.geometry("1100x750")

        # Dữ liệu lưu trữ
        self.G_matrix = []
        self.nodes = []
        self.nx_graph = None
        self.pos = None # Vị trí vẽ

        self._setup_ui()

    def _setup_ui(self):
        # 1. Khung bên trái (Control Panel)
        control_frame = ttk.LabelFrame(self.root, text="Điều khiển", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Input số lượng
        ttk.Label(control_frame, text="Số đỉnh / Kích thước cạnh:").pack(anchor="w")
        self.entry_size = ttk.Entry(control_frame)
        self.entry_size.insert(0, "10")
        self.entry_size.pack(fill=tk.X, pady=5)

        # Input xác suất (cho random)
        ttk.Label(control_frame, text="Tỉ lệ nối cạnh (0.0 - 1.0):").pack(anchor="w")
        self.entry_prob = ttk.Entry(control_frame)
        self.entry_prob.insert(0, "0.3")
        self.entry_prob.pack(fill=tk.X, pady=5)

        # Input màu
        ttk.Label(control_frame, text="Danh sách màu (Tiếng Anh):").pack(anchor="w")
        self.entry_colors = ttk.Entry(control_frame)
        self.entry_colors.insert(0, "red blue green yellow orange purple cyan")
        self.entry_colors.pack(fill=tk.X, pady=5)

        ttk.Separator(control_frame).pack(fill='x', pady=15)

        # Các nút bấm
        ttk.Button(control_frame, text="1. Tạo Đồ Thị Ngẫu Nhiên", command=self.btn_random_click).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="2. Tạo Bàn Cờ (Lưới)", command=self.btn_grid_click).pack(fill=tk.X, pady=5)
        
        ttk.Separator(control_frame).pack(fill='x', pady=15)
        
        self.btn_solve = ttk.Button(control_frame, text="3. TÔ MÀU (SOLVE)", command=self.btn_solve_click, state=tk.DISABLED)
        self.btn_solve.pack(fill=tk.X, pady=10)

        self.lbl_status = ttk.Label(control_frame, text="Sẵn sàng...", foreground="blue", wraplength=200)
        self.lbl_status.pack(pady=20)

        # 2. Khung bên phải (Vẽ hình)
        display_frame = ttk.Frame(self.root)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nhúng Matplotlib vào Tkinter
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def btn_random_click(self):
        try:
            n = int(self.entry_size.get())
            p = float(self.entry_prob.get())
            if n <= 0 or not (0 <= p <= 1): raise ValueError
            
            # Gọi hàm từ file algorithms
            self.nx_graph, self.nodes, self.G_matrix = algo.tao_do_thi_ngau_nhien(n, p)
            
            # Tính toán vị trí vẽ đẹp nhất
            self.pos = nx.spring_layout(self.nx_graph, seed=42)
            
            self.draw_graph()
            self.lbl_status.config(text=f"Đồ thị ngẫu nhiên: {n} đỉnh.")
            self.btn_solve.config(state=tk.NORMAL)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

    def btn_grid_click(self):
        try:
            side = int(self.entry_size.get())
            if side <= 0: raise ValueError
            
            # Gọi hàm từ file algorithms
            self.nx_graph, self.nodes, self.G_matrix = algo.tao_do_thi_luoi(side)
            
            # Tính toán vị trí vẽ dạng lưới
            self.pos = {node: (int(node.split(',')[1]), -int(node.split(',')[0])) for node in self.nodes}
            
            self.draw_graph()
            self.lbl_status.config(text=f"Bàn cờ kích thước {side}x{side}.")
            self.btn_solve.config(state=tk.NORMAL)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Kích thước cạnh phải là số nguyên dương!")

    def btn_solve_click(self):
        # Lấy màu từ input
        raw_colors = self.entry_colors.get().strip().split()
        if not raw_colors: raw_colors = ["red", "green", "blue", "yellow"]
        
        # Gọi hàm xử lý chính từ file algorithms
        solution = algo.thuc_hien_to_mau(self.nodes, self.G_matrix, raw_colors)
        
        # Chuyển kết quả dictionary thành list màu theo đúng thứ tự đỉnh để vẽ
        color_map = [solution.get(node, 'white') for node in self.nodes]
        
        # Vẽ lại với màu mới
        self.draw_graph(node_colors=color_map)
        
        # Thống kê
        used_colors = set(solution.values())
        if 'white' in used_colors: used_colors.remove('white')
        
        msg = f"Đã tô xong!\nSố màu sử dụng: {len(used_colors)}"
        self.lbl_status.config(text=msg)
        messagebox.showinfo("Kết quả", msg)

    def draw_graph(self, node_colors='lightgray'):
        self.ax.clear()
        
        # Vẽ bằng networkx
        nx.draw(self.nx_graph, pos=self.pos, ax=self.ax,
                with_labels=True,
                node_color=node_colors,
                node_size=500,
                font_size=8,
                edge_color='gray',
                font_color='black' if node_colors == 'lightgray' else 'black')
        
        self.canvas.draw()