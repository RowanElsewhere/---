import pyautogui
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("自动点击器")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.recorded_positions = []
        self.is_recording = False
        self.is_running = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.max_positions = 6
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="自动点击器", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.record_btn = ttk.Button(control_frame, text="开始录制", command=self.toggle_recording)
        self.record_btn.pack(fill=tk.X, pady=5)
        
        self.execute_btn = ttk.Button(control_frame, text="开始执行", command=self.start_execution, state=tk.DISABLED)
        self.execute_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = ttk.Button(control_frame, text="停止执行", command=self.stop_execution, state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        settings_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        max_pos_frame = ttk.Frame(settings_frame)
        max_pos_frame.pack(fill=tk.X, pady=5)
        ttk.Label(max_pos_frame, text="最大位置数:").pack(side=tk.LEFT)
        self.max_pos_var = tk.StringVar(value="6")
        self.max_pos_entry = ttk.Entry(max_pos_frame, textvariable=self.max_pos_var, width=10)
        self.max_pos_entry.pack(side=tk.RIGHT)
        
        repeat_frame = ttk.Frame(settings_frame)
        repeat_frame.pack(fill=tk.X, pady=5)
        ttk.Label(repeat_frame, text="重复次数:").pack(side=tk.LEFT)
        self.repeat_var = tk.StringVar(value="1")
        ttk.Entry(repeat_frame, textvariable=self.repeat_var, width=10).pack(side=tk.RIGHT)
        
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        ttk.Label(interval_frame, text="间隔时间(秒):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="1.0")
        ttk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(side=tk.RIGHT)
        
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="就绪", foreground="blue")
        self.status_label.pack()
        
        self.position_count_label = ttk.Label(status_frame, text="已记录位置: 0/6")
        self.position_count_label.pack()
        
        list_frame = ttk.LabelFrame(main_frame, text="已记录位置", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.position_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.position_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.position_list.yview)
        
        clear_btn = ttk.Button(main_frame, text="清空记录", command=self.clear_positions)
        clear_btn.pack(fill=tk.X, pady=(10, 0))
        
        help_label = ttk.Label(main_frame, text="快捷键: ESC 停止执行", font=("Arial", 9), foreground="gray")
        help_label.pack(pady=(10, 0))
        
        self.setup_keyboard_listener()
        
    def setup_keyboard_listener(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                self.stop_execution()
        
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        try:
            self.max_positions = int(self.max_pos_var.get())
        except ValueError:
            messagebox.showerror("错误", "最大位置数必须是整数！")
            return
        
        if self.max_positions < 1:
            messagebox.showerror("错误", "最大位置数必须大于0！")
            return
        
        self.max_pos_entry.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.DISABLED)
        self.position_count_label.config(text=f"已记录位置: 0/{self.max_positions}")
        self.countdown = 3
        self.do_countdown()
        
    def do_countdown(self):
        if self.countdown > 0:
            self.status_label.config(text=f"{self.countdown} 秒后开始录制...", foreground="orange")
            self.countdown -= 1
            self.root.after(1000, self.do_countdown)
        else:
            self.is_recording = True
            self.record_btn.config(text="停止录制", state=tk.NORMAL)
            self.status_label.config(text="录制中... 请点击屏幕", foreground="green")
            
            def on_click(x, y, button, pressed):
                if pressed and self.is_recording:
                    if len(self.recorded_positions) >= self.max_positions:
                        self.root.after(0, self.stop_recording)
                        return
                    self.recorded_positions.append((x, y))
                    self.position_list.insert(tk.END, f"位置 {len(self.recorded_positions)}: ({x}, {y})")
                    self.position_count_label.config(text=f"已记录位置: {len(self.recorded_positions)}/{self.max_positions}")
                    self.execute_btn.config(state=tk.NORMAL)
                    if len(self.recorded_positions) >= self.max_positions:
                        self.root.after(0, self.stop_recording)
            
            self.mouse_listener = mouse.Listener(on_click=on_click)
            self.mouse_listener.start()
        
    def stop_recording(self):
        self.is_recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.record_btn.config(text="开始录制")
        self.max_pos_entry.config(state=tk.NORMAL)
        self.status_label.config(text=f"录制完成，共 {len(self.recorded_positions)} 个位置", foreground="blue")
        
    def clear_positions(self):
        self.recorded_positions = []
        self.position_list.delete(0, tk.END)
        self.position_count_label.config(text=f"已记录位置: 0/{self.max_positions}")
        self.execute_btn.config(state=tk.DISABLED)
        self.status_label.config(text="记录已清空", foreground="blue")
        
    def start_execution(self):
        if len(self.recorded_positions) == 0:
            messagebox.showwarning("警告", "请先录制点击位置！")
            return
            
        try:
            repeat_count = int(self.repeat_var.get())
            interval = float(self.interval_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            return
            
        if repeat_count < 1:
            messagebox.showerror("错误", "重复次数必须大于0！")
            return
            
        if interval < 0:
            messagebox.showerror("错误", "间隔时间不能为负数！")
            return
            
        self.is_running = True
        self.execute_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.record_btn.config(state=tk.DISABLED)
        self.status_label.config(text="执行中...", foreground="green")
        
        def execute_thread():
            for round_num in range(1, repeat_count + 1):
                if not self.is_running:
                    break
                    
                self.root.after(0, lambda r=round_num: self.status_label.config(text=f"执行中... 第 {r}/{repeat_count} 轮", foreground="green"))
                
                for i, (x, y) in enumerate(self.recorded_positions, 1):
                    if not self.is_running:
                        break
                        
                    self.root.after(0, lambda p=i, pos=(x, y): self.status_label.config(text=f"执行中... 点击位置 {p}/{len(self.recorded_positions)}: {pos}", foreground="green"))
                    pyautogui.click(x, y)
                    
                    if i < len(self.recorded_positions) or round_num < repeat_count:
                        time.sleep(interval)
            
            if self.is_running:
                self.root.after(0, lambda: self.status_label.config(text="执行完成！", foreground="green"))
                self.root.after(0, lambda: messagebox.showinfo("完成", "自动点击执行完成！"))
            
            self.root.after(0, self.execution_finished)
        
        threading.Thread(target=execute_thread, daemon=True).start()
        
    def stop_execution(self):
        self.is_running = False
        self.status_label.config(text="已停止", foreground="red")
        
    def execution_finished(self):
        self.execute_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.NORMAL)
        self.is_running = False
        
    def on_closing(self):
        self.is_running = False
        self.is_recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
