import os
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
from dataclasses import dataclass
from typing import Literal


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{CUR_F_NAME}.log', encoding='utf-8')
        ]
    )

    logging.info('Logging setup complete')


@dataclass
class AppState:
    watermark: Image.Image = None
    target: Image.Image = None
    opacity: tk.DoubleVar = None
    x_offset: tk.DoubleVar = None
    y_offset: tk.DoubleVar = None
    filetypes: tuple = (("Image files", "*.png *.jpg *.jpeg *.bmp"),)


class WatermarkApp:
    def __init__(self, root: tk.Tk):
        logging.info('Initializing app...')

        self.root = root
        self.root.title('Watermark App')
        self.root.minsize(600, 500)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.state = AppState(
            opacity=tk.DoubleVar(value=0.5),
            x_offset=tk.DoubleVar(value=20),
            y_offset=tk.DoubleVar(value=20)
        )

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill='both', expand=True, pady=10)

        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self._setup_controls()

        self.status = tk.StringVar(value='Ready')
        ttk.Label(self.root, textvariable=self.status, anchor='w').pack(fill='x', side='bottom')

        self._toggle_sliders('disabled')

        logging.info('App UI Initialized')

    def _setup_controls(self):
        logging.info('Setting up controls...')

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text='Upload Image', command=self.load_target_image).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text='Upload Watermark', command=self.load_watermark).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text='Save Image', command=self.save_image).grid(row=0, column=2, padx=5)

        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(pady=5)

        tk.Label(slider_frame, text='Opacity').grid(row=0, column=0)
        self.opacity_slider = ttk.Scale(
            slider_frame, from_=0, to=1,
            variable=self.state.opacity, orient='horizontal',
            command=self._on_slider_change
        )
        self.opacity_slider.grid(row=0, column=1, padx=10)

        ttk.Label(slider_frame, text='Right Margin (X Offset)').grid(row=0, column=2)
        self.x_offset_slider = ttk.Scale(
            slider_frame, from_=0, to=200, variable=self.state.x_offset,
            orient='horizontal', command=self._on_slider_change
        )
        self.x_offset_slider.grid(row=0, column=3, padx=10)

        ttk.Label(slider_frame, text='Bottom Margin (Y Offset)').grid(row=0, column=4)
        self.y_offset_slider = ttk.Scale(
            slider_frame, from_=0, to=200, variable=self.state.y_offset,
            orient='horizontal', command=self._on_slider_change
        )
        self.y_offset_slider.grid(row=0, column=5, padx=10)

        logging.info('Controls setup complete')

    def _toggle_sliders(self, state: Literal['normal', 'active', 'disabled'] = 'normal'):
        self.opacity_slider.configure(state=state)
        self.x_offset_slider.configure(state=state)
        self.y_offset_slider.configure(state=state)

    def load_target_image(self):
        logging.info('Loading target image...')
        path = filedialog.askopenfilename(filetypes=self.state.filetypes)
        if not path:
            logging.warning('No image selected')
            if not self.state.target:
                messagebox.showwarning("Missing data", "Please select image to load")
            return

        img = Image.open(path).convert("RGBA")
        self.state.target = img
        logging.info(f'Target image loaded from: {path}')
        messagebox.showinfo("Image Loaded", "Target image loaded successfully.")
        self._refresh_canvas()

    def load_watermark(self):
        logging.info('Loading watermark...')
        path = filedialog.askopenfilename(filetypes=self.state.filetypes)
        if not path:
            logging.warning('No watermark selected')
            if not self.state.watermark:
                messagebox.showwarning('Missing data', 'Please select watermark to load')
            return

        wm = Image.open(path).convert('RGBA')
        wm.thumbnail((150, 150))
        self.state.watermark = wm
        logging.info(f'Watermark loaded from: {path}')
        messagebox.showinfo("Watermark Loaded", "Watermark image loaded successfully.")

        self._toggle_sliders('active')
        self._refresh_canvas()

    def apply_watermark(self) -> Image.Image:
        logging.info('Applying watermark')

        if not self.state.target or not self.state.watermark:
            logging.info('No target image or watermark found')
            return self.state.target

        base_img = self.state.target.copy()
        wm_img = self.state.watermark.copy()

        alpha = wm_img.getchannel("A")
        alpha = ImageEnhance.Brightness(alpha).enhance(self.state.opacity.get())
        wm_img.putalpha(alpha)

        pos = (
            base_img.width - wm_img.width - int(self.state.x_offset.get()),
            base_img.height - wm_img.height - int(self.state.y_offset.get())
        )

        base_img.paste(wm_img, pos, wm_img)
        logging.info('Watermark applied successfully')

        return base_img

    def _refresh_canvas(self):
        logging.info('Refreshing canvas')

        if not self.state.target:
            return

        img_to_show = self.apply_watermark() if self.state.watermark else self.state.target.copy()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10 or canvas_height < 10:
            return  # Avoid rendering in tiny or invalid sizes

        resized = img_to_show.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized)

        self.canvas.img = tk_img  # prevent garbage collection
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=tk_img)

        logging.info('Canvas refreshed')

    def _on_slider_change(self, _=None):
        self._refresh_canvas()

    def _on_canvas_resize(self, event):
        self._refresh_canvas()

    def save_image(self):
        logging.info('Saving image')

        if not self.state.target or not self.state.watermark:
            logging.warning('Target image/Watermark missing')
            messagebox.showwarning("Missing data", "Please load both an image and a watermark.")
            return

        final_img = self.apply_watermark()
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=self.state.filetypes)
        if not path:
            logging.info('Save cancelled')
            return

        final_img.convert('RGB').save(path)

        logging.info(f"Image saved to: {path}")
        messagebox.showinfo("Image Saved", f"Image saved to:\n{path}")


def main():
    setup_logging()

    logging.info('Starting Watermark App...')

    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

    logging.info('App closed')


if __name__ == '__main__':
    CUR_F_NAME = os.path.splitext(os.path.basename(__file__))[0]
    main()

    # TODO: resize canvas to image size
    # TODO: Need to make this proper