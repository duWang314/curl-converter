import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

import pyperclip

from curl_parser import curl_to_python


class CurlConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Curl Converter")
        self.root.geometry("800x600")
        
        # 设置主题和样式
        self.style = ttk.Style()
        self.style.configure("TButton")
        self.style.configure("TLabel")
        
        # 创建界面
        self.create_widgets()
        
        # 绑定快捷键
        self.root.bind("<Control-v>", self.paste_from_clipboard)
        self.root.bind("<Control-c>", self.copy_to_clipboard)
        
    def create_widgets(self):
        # 创建一个主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个水平分割器
        panedwindow = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        panedwindow.pack(fill=tk.BOTH, expand=True)
        
        # 上半部分：输入区域
        input_frame = ttk.LabelFrame(panedwindow, text="Input curl command")
        panedwindow.add(input_frame, weight=1)
        
        # Curl 输入文本框
        self.curl_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, font=("Consolas", 10))
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)

        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_columnconfigure(0, weight=1)
        self.curl_input.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        button_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # 转换按钮
        convert_button = ttk.Button(button_frame, text=">>convert<<", command=self.convert_curl)
        convert_button.pack(side=tk.LEFT, padx=5)
        
        # 粘贴按钮
        paste_button = ttk.Button(button_frame, text="paste from clipboard", command=self.paste_from_clipboard)
        paste_button.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="clear input", command=self.clear_input)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 打开文件按钮
        open_button = ttk.Button(button_frame, text="open file", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=5)
        
        # 下半部分：输出区域
        output_frame = ttk.LabelFrame(panedwindow, text="Python request element")
        panedwindow.add(output_frame, weight=1)
        
        # Python 输出文本框
        self.python_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10))
        
        # 输出按钮区域
        output_button_frame = ttk.Frame(output_frame)

        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        self.python_output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        output_button_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # 复制按钮
        copy_button = ttk.Button(output_button_frame, text="copy to clipboard", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=5)
        
        # 保存到文件按钮
        save_button = ttk.Button(output_button_frame, text="save to file", command=self.save_to_file)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 清空输出按钮
        clear_output_button = ttk.Button(output_button_frame, text="clear output", command=self.clear_output)
        clear_output_button.pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def convert_curl(self):
        """转换curl命令为Python请求元素"""
        curl_cmd = self.curl_input.get("1.0", tk.END).strip()
        if not curl_cmd:
            messagebox.showwarning("WARNING", "Please enter the curl command!")
            return
        
        try:
            # 使用解析器转换curl命令
            python_code = curl_to_python(curl_cmd)
            
            # 显示结果
            self.python_output.delete("1.0", tk.END)
            self.python_output.insert("1.0", python_code)
            
            self.status_var.set("convert")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to convert: {str(e)}")
            self.status_var.set(f"Failed to convert: {str(e)}")
    
    def paste_from_clipboard(self):
        """从剪贴板粘贴内容到输入区域"""
        try:
            clipboard_text = pyperclip.paste()
            self.curl_input.delete("1.0", tk.END)
            self.curl_input.insert("1.0", clipboard_text)
            self.status_var.set("pasted from clipboard")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to paste: {str(e)}")
    
    def copy_to_clipboard(self):
        """复制输出内容到剪贴板"""
        try:
            output_text = self.python_output.get("1.0", tk.END).strip()
            if output_text:
                pyperclip.copy(output_text)
                self.status_var.set("copied to clipboard")
            else:
                messagebox.showwarning("WARING", "There is nothing to copy!")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to copy: {str(e)}")
    
    def clear_input(self):
        """清空输入区域"""
        self.curl_input.delete("1.0", tk.END)
        self.status_var.set("input cleared")
    
    def clear_output(self):
        """清空输出区域"""
        self.python_output.delete("1.0", tk.END)
        self.status_var.set("output cleared")
    
    def open_file(self):
        """打开文件并读取内容"""
        file_path = filedialog.askopenfilename(
            title="select a file",
            filetypes=[("text file", "*.txt"), ("all", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.curl_input.delete("1.0", tk.END)
                    self.curl_input.insert("1.0", content)
                    self.status_var.set(f"opened file: {file_path}")
            except Exception as e:
                messagebox.showerror("ERROR", f"Failed to open the file: {str(e)}")
    
    def save_to_file(self):
        """保存输出内容到文件"""
        output_text = self.python_output.get("1.0", tk.END).strip()
        if not output_text:
            messagebox.showwarning("WARNING", "There is nothing to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="save as file",
            defaultextension=".py",
            filetypes=[("Python file", "*.py"), ("text file", "*.txt"), ("all", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(output_text)
                    self.status_var.set(f"saved to file: {file_path}")
            except Exception as e:
                messagebox.showerror("ERROR", f"Failed to save as a file: {str(e)}")


def main():
    root = tk.Tk()
    CurlConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
