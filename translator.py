import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Define a comprehensive key mapping dictionary based on pynput key names
key_mappings = {
    'Key.space': ' ',
    'Key.enter': '\n',
    'Key.tab': '\t',
    'Key.backspace': '[BACKSPACE]',
    'Key.shift': '[SHIFT]',
    'Key.shift_r': '[SHIFT]',
    'Key.cmd': '[WIN]',
    'Key.cmd_r': '[WIN]',
    'Key.ctrl_l': '[CTRL]',
    'Key.ctrl_r': '[CTRL]',
    'Key.alt_l': '[ALT]',
    'Key.alt_r': '[ALT]',
    'Key.delete': '[DEL]',
    'Key.print_screen': '[PRINT_SCREEN]',
    'Key.esc': '[ESC]',
    'Key.up': '[UP]',
    'Key.down': '[DOWN]',
    'Key.left': '[LEFT]',
    'Key.right': '[RIGHT]',
    'Key.home': '[HOME]',
    'Key.end': '[END]',
    'Key.page_up': '[PAGE_UP]',
    'Key.page_down': '[PAGE_DOWN]',
    'Key.insert': '[INSERT]',
    'Key.f1': '[F1]',
    'Key.f2': '[F2]',
    'Key.f3': '[F3]',
    'Key.f4': '[F4]',
    'Key.f5': '[F5]',
    'Key.f6': '[F6]',
    'Key.f7': '[F7]',
    'Key.f8': '[F8]',
    'Key.f9': '[F9]',
    'Key.f10': '[F10]',
    'Key.f11': '[F11]',
    'Key.f12': '[F12]',
    'Key.caps_lock': '[CAPS_LOCK]',
    'Key.num_lock': '[NUM_LOCK]',
    'Key.scroll_lock': '[SCROLL_LOCK]',
    'Key.pause': '[PAUSE]',
    'Key.menu': '[MENU]',
    'Key.windows': '[WIN]'
}

def read_keylog(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def translate_keylog(lines):
    translation = []
    current_line = []
    shift_active = False

    for line in lines:
        key_event = line.strip()
        if key_event in key_mappings:
            if key_event in ('Key.shift', 'Key.shift_r'):
                shift_active = True
            else:
                current_line.append(key_mappings[key_event])
        elif re.match(r'^Key\.', key_event):
            current_line.append(f'[{key_event.split(".")[1].upper()}]')
        else:
            if shift_active:
                current_line.append(key_event.upper())
                shift_active = False
            else:
                current_line.append(key_event)

    translation.append(''.join(current_line))
    return ''.join(translation)

def main():
    # Hide the root window
    Tk().withdraw()
    # Ask the user to select a file
    log_file_path = askopenfilename(title="Select the log file", filetypes=[("Text files", "*.txt")])
    
    if not log_file_path:
        print("No file selected. Exiting.")
        return
    
    keylog_lines = read_keylog(log_file_path)
    translation = translate_keylog(keylog_lines)
    print(translation)

if __name__ == '__main__':
    main()
