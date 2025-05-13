import mss
from datetime import datetime
from PIL import Image
import io
import platform
import os
from core.registry import register_command

@register_command(r"screenshot", needs_input=False)
def take_ultimate_screenshot(
    watermark_path="core/watermark.png",
    to_clipboard=True,
    all_monitors=False,
    filename=None,
    save_folder=os.path.join(os.path.expanduser("~"), "Desktop", "byjarvis", "Screenshots"),
    auto_open=True
):
    try:
        os.makedirs(save_folder, exist_ok=True)

        with mss.mss() as sct:
            monitor = sct.monitors[0] if all_monitors else sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb).convert("RGBA")

        # Apply watermark if available
        if os.path.exists(watermark_path):
            try:
                watermark = Image.open(watermark_path).convert("RGBA")
                scale_factor = 0.2
                new_w = int(img.width * scale_factor)
                new_h = int(new_w * watermark.height / watermark.width)
                watermark = watermark.resize((new_w, new_h), Image.LANCZOS)
                position = (img.width - new_w - 20, img.height - new_h - 20)
                img.alpha_composite(watermark, position)
            except Exception as e:
                print(f"⚠️ Failed to apply watermark: {e}")
        else:
            print(f"⚠️ Watermark not found: {watermark_path}")

        # Generate filename if not provided
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(save_folder, filename)

        # Save image
        img.save(filepath)
        print(f"✅ Screenshot saved: {filepath}")

        # Copy to clipboard (Windows only)
        if to_clipboard and platform.system() == "Windows":
            try:
                output = io.BytesIO()
                img.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]  # Remove BMP header
                output.close()

                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                print("📋 Screenshot copied to clipboard.")
            except Exception as e:
                print(f"⚠️ Clipboard copy failed: {e}")

        # Open the image (optional)
        if auto_open:
            os.startfile(filepath) if platform.system() == "Windows" else os.system(f'xdg-open "{filepath}"')

        return filepath

    except Exception as err:
        print(f"❌ Screenshot failed: {err}")
        return None

# 🚀 Fire it up!
# take_ultimate_screenshot()
