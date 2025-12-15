import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog # <--- Đã thêm filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import hashlib 
import algorithms as algo 

# Bảng màu mặc định ban đầu
DEFAULT_COLORS = {
    'Red': '#e74c3c', 'Green': '#2ecc71', 'Blue': '#3498db',
    'Yellow': '#f1c40f', 'Orange': '#e67e22', 'Purple': '#9b59b6',
    'Cyan': '#1abc9c', 'Gray': '#95a5a6'
}

class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring - Pro Version")
        self.root.geometry("1150x780") # Tăng chiều cao một chút để chứa nút Lưu
        
        self.bg_color = "#F0F2F5" 
        self.root.configure(bg=self.bg_color)

        self.G_matrix = []
        self.nodes = []
        self.nx_graph = None
        self.pos = None 
        
        self.color_vars = {}     
        self.custom_colors = {}  
        
        self.chk_row = 0
        self.chk_col = 0

        self._setup_styles()
        self._setup_ui()
        
        # Khởi tạo màu mặc định
        for name, hex_code in DEFAULT_COLORS.items():
            self.add_color_checkbox(name, hex_code)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style cho khung nền trắng
        style.configure("Card.TFrame", background="white", relief="flat")
        
        # Style cho Tiêu đề và Nhãn
        style.configure("Header.TLabel", background="white", foreground="#2C3E50", font=("Segoe UI", 12, "bold"))
        style.configure("Label.TLabel", background="white", foreground="#7F8C8D", font=("Segoe UI", 10))
        
        # --- NÚT PRIMARY (Dùng cho nút TẠO ĐỒ THỊ & LƯU ẢNH) ---
        style.configure("Primary.TButton", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#3498DB",   # Nền Xanh dương
                        foreground="white",     # Chữ Trắng
                        borderwidth=0)
        # Map: Khi di chuột (active) vẫn giữ nền xanh đậm và chữ trắng
        style.map("Primary.TButton", 
                  background=[('active', '#2980B9')], 
                  foreground=[('active', 'white')]) 
        
        # --- NÚT SUCCESS (Dùng cho nút THỰC HIỆN TÔ MÀU) ---
        style.configure("Success.TButton", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#2ECC71",   # Nền Xanh lá
                        foreground="white",     # Chữ Trắng
                        borderwidth=0)
        # Map: Khi di chuột (active) vẫn giữ nền xanh đậm và chữ trắng
        style.map("Success.TButton", 
                  background=[('active', '#27AE60')],
                  foreground=[('active', 'white')])
        
        # --- NÚT ADD (Dùng cho nút Thêm màu) ---
        style.configure("Add.TButton", 
                        font=("Segoe UI", 9), 
                        background="#95a5a6", 
                        foreground="white", 
                        borderwidth=0)
        style.map("Add.TButton", 
                  background=[('active', '#7f8c8d')],
                  foreground=[('active', 'white')])
        
    def _setup_ui(self):
        # --- SIDEBAR ---
        sidebar = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        sidebar.place(relx=0.02, rely=0.03, relwidth=0.32, relheight=0.94)

        ttk.Label(sidebar, text="1. CẤU HÌNH ĐỒ THỊ", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        ttk.Label(sidebar, text="Số đỉnh:", style="Label.TLabel").pack(anchor="w")
        self.entry_nodes = ttk.Entry(sidebar, font=("Segoe UI", 11))
        self.entry_nodes.insert(0, "15") # Mặc định 15 cho đẹp
        self.entry_nodes.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(sidebar, text="Độ phức tạp (0.1 - 1.0):", style="Label.TLabel").pack(anchor="w")
        self.entry_prob = ttk.Entry(sidebar, font=("Segoe UI", 11))
        self.entry_prob.insert(0, "0.4")
        self.entry_prob.pack(fill=tk.X, pady=(0, 15))

        self.btn_create = ttk.Button(sidebar, text="TẠO ĐỒ THỊ", style="Primary.TButton", command=self.btn_create_click)
        self.btn_create.pack(fill=tk.X, ipady=5)

        ttk.Separator(sidebar).pack(fill='x', pady=15)

        ttk.Label(sidebar, text="2. KHO MÀU SẮC", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
  
        self.checkbox_container = tk.Frame(sidebar, bg="white")
        self.checkbox_container.pack(fill=tk.BOTH, expand=True)

        self.btn_add_color = ttk.Button(sidebar, text="+ Thêm màu tùy chọn...", style="Add.TButton", command=self.btn_add_custom_color)
        self.btn_add_color.pack(fill=tk.X, pady=10)

        # Nút Tô màu
        self.btn_solve = ttk.Button(sidebar, text="THỰC HIỆN TÔ MÀU", style="Success.TButton", command=self.btn_solve_click, state=tk.DISABLED)
        self.btn_solve.pack(fill=tk.X, ipady=8, pady=(10, 5))

        # --- NÚT LƯU ẢNH (Mới thêm) ---
        self.btn_save = ttk.Button(sidebar, text="💾 LƯU ẢNH KẾT QUẢ", style="Primary.TButton", command=self.btn_save_click, state=tk.DISABLED)
        self.btn_save.pack(fill=tk.X, ipady=5, pady=5)
        # ------------------------------

        # Status
        self.lbl_status = tk.Label(sidebar, text="...", bg="#ECF0F1", fg="#7F8C8D", font=("Consolas", 9), justify="left", anchor="nw")
        self.lbl_status.pack(fill=tk.BOTH, expand=True)

        # --- MAIN DISPLAY ---
        display_frame = tk.Frame(self.root, bg=self.bg_color)
        display_frame.place(relx=0.36, rely=0.03, relwidth=0.62, relheight=0.94)

        self.fig, self.ax = plt.subplots(figsize=(6, 6), facecolor=self.bg_color)
        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.axis('off')

    def add_color_checkbox(self, name, hex_code):
        if name in self.custom_colors: return 

        self.custom_colors[name] = hex_code
        var = tk.BooleanVar(value=True)
        self.color_vars[name] = var
        
        chk = tk.Checkbutton(self.checkbox_container, 
                             text=name, 
                             variable=var, 
                             bg="white", 
                             fg=hex_code, 
                             font=("Segoe UI", 10, "bold"),
                             activebackground="white",
                             selectcolor="white",
                             anchor="w")
        
        chk.grid(row=self.chk_row, column=self.chk_col, sticky="w", padx=5, pady=2)
        
        self.chk_col += 1
        if self.chk_col > 1:
            self.chk_col = 0
            self.chk_row += 1

    def btn_add_custom_color(self):
        color_code = colorchooser.askcolor(title="Chọn màu mới")[1] 
        if color_code:
            self.add_color_checkbox(color_code, color_code)

    def btn_create_click(self):
        try:
            n = int(self.entry_nodes.get())
            p = float(self.entry_prob.get())
            if n <= 0 or not (0 < p <= 1): raise ValueError

            self.nx_graph, self.nodes, self.G_matrix = algo.tao_do_thi_ngau_nhien(n, p)
            self.pos = nx.spring_layout(self.nx_graph, k=0.9, seed=42)
            
            self.draw_graph(node_colors='#34495e')
            self.lbl_status.config(text=f"✓ Đã tạo {n} đỉnh.\n-> Chọn màu rồi bấm nút xanh.")
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.DISABLED) # Khi tạo mới thì khóa nút lưu lại
        except ValueError:
            messagebox.showerror("Lỗi", "Thông số không hợp lệ.")

    def btn_solve_click(self):
        selected_colors_names = [name for name, var in self.color_vars.items() if var.get()]
        
        if not selected_colors_names:
            messagebox.showwarning("Chú ý", "Bạn phải chọn ít nhất 1 màu!")
            return

        solution = algo.giai_thuat_to_mau_ha_bac(self.nodes, self.G_matrix, selected_colors_names)
        
        final_colors = []
        for node in self.nodes:
            color_name = solution.get(node, 'gray')
            hex_code = self.custom_colors.get(color_name, '#95a5a6') 
            final_colors.append(hex_code)
        
        self.draw_graph(node_colors=final_colors)
        
        used = set(solution.values())
        self.lbl_status.config(text=f"XONG!\nSố màu dùng: {len(used)}")
        
        # Mở khóa nút Lưu ảnh
        self.btn_save.config(state=tk.NORMAL)

    def btn_save_click(self):
        """Hàm xử lý lưu ảnh"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Lưu ảnh đồ thị"
        )
        
        if file_path:
            try:
                # Lưu hình với chất lượng cao (dpi=300)
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor=self.bg_color)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh tại:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không lưu được ảnh: {e}")

    def draw_graph(self, node_colors):
        self.ax.clear()
        nx.draw_networkx_edges(self.nx_graph, self.pos, ax=self.ax, width=1.5, alpha=0.6, edge_color="#95a5a6")
        nx.draw_networkx_nodes(self.nx_graph, self.pos, ax=self.ax, node_color=node_colors, node_size=700, edgecolors='white', linewidths=2)
        nx.draw_networkx_labels(self.nx_graph, self.pos, ax=self.ax, font_size=9, font_weight="bold", font_color='white')
        self.ax.axis('off')
        self.canvas.draw()