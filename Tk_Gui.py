import tkinter as tk
from tkinter import ttk
from ssh_utils import SSHClient

class SSHSessionTab:
    def __init__(self, notebook, name):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=name)

        self.ssh = None

        # Frame trái nhập thông tin SSH
        frame_left = ttk.LabelFrame(self.frame, text="Thông tin kết nối", padding=10)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(frame_left, text="IP:").pack()
        self.entry_ip = ttk.Entry(frame_left)
        self.entry_ip.pack()

        ttk.Label(frame_left, text="Username:").pack()
        self.entry_user = ttk.Entry(frame_left)
        self.entry_user.pack()

        ttk.Label(frame_left, text="Password:").pack()
        self.entry_pass = ttk.Entry(frame_left, show="*")
        self.entry_pass.pack()

        self.btn_connect = ttk.Button(frame_left, text="Kết nối", command=self.connect_ssh)
        self.btn_connect.pack(pady=5)

        # Frame phải: Terminal
        frame_right = ttk.LabelFrame(self.frame, text="Terminal", padding=10)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_output = tk.Text(
            frame_right,
            bg="#1e1e1e",
            fg="yellow",
            insertbackground="white",
            wrap=tk.WORD,
            font=("Courier", 10, "bold")
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        self.text_output.config(state=tk.DISABLED)

        self.entry_command = tk.Entry(
            frame_right,
            bg="#1e1e1e",
            fg="yellow",
            insertbackground="white",
            font=("Courier", 10, "bold")
        )
        self.entry_command.pack(fill=tk.X)
        self.entry_command.bind("<Return>", self.send_command)

        self.text_output.tag_configure("command", foreground="deep sky blue", font=("Courier", 10, "bold"))
        self.text_output.tag_configure("output", foreground="yellow", font=("Courier", 10, "bold"))

    def connect_ssh(self):
        ip = self.entry_ip.get()
        user = self.entry_user.get()
        passwd = self.entry_pass.get()

        try:
            self.ssh = SSHClient(ip, user, passwd)
            self.ssh.connect()
            self.append_output(f"Kết nối thành công tới {user}@{ip}", tag="output")
        except Exception as e:
            self.append_output(f"Lỗi kết nối: {str(e)}", tag="output")

    def send_command(self, event=None):
        cmd = self.entry_command.get()
        if self.ssh:
            output = self.ssh.send_command(cmd)
            self.append_output(f"> {cmd}", tag="command")
            self.append_output(output, tag="output")
        else:
            self.append_output("Chưa kết nối SSH.", tag="output")
        self.entry_command.delete(0, tk.END)

    def append_output(self, text, tag="output"):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(tk.END, text + "\n", tag)
        self.text_output.see(tk.END)
        self.text_output.config(state=tk.DISABLED)

class SSHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Multi-Session GUI")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e1e")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.session_counter = 0

        btn_new = ttk.Button(root, text="➕ Tạo phiên mới", command=self.new_session)
        btn_new.pack(side=tk.TOP, pady=5)

        self.new_session()  # Tạo sẵn 1 phiên đầu

    def new_session(self):
        self.session_counter += 1
        SSHSessionTab(self.notebook, f"Phiên {self.session_counter}")
