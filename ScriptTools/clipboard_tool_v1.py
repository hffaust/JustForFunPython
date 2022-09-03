import pyautogui as pya
import pyperclip  # handy cross-platform clipboard text handler
import time
import keyboard
import win32clipboard
import time

'''
    References:
        1. http://timgolden.me.uk/pywin32-docs/win32clipboard.html
        2. https://stackoverflow.com/questions/34156041/how-to-paste-text-from-the-clipboard-into-a-text-field
        3. https://stackoverflow.com/questions/40439917/modifying-a-clipboard-content-to-be-treated-as-html
        4. https://abdus.dev/posts/monitor-clipboard/
        5. https://stackoverflow.com/questions/34514644/in-python-3-how-can-i-tell-if-windows-is-locked/43758104
        6. https://nitratine.net/blog/post/how-to-make-hotkeys-in-python/
        7. https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
'''

lst = []
def copy_clipboard():
    pyperclip.copy("") # <- This prevents last copy replacing current copy of null.
    pya.hotkey('ctrl', 'c')
    time.sleep(0.1)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()

def double_click_copy():
    # double clicks on a position of the cursor
    pya.doubleClick(pya.position())

    var = copy_clipboard()
    lst.append(var)
    print(lst)



def char_to_ascii_print(data):
    print("="*64)
    print(data)
    print("-"*64)
    #chars       = []
    #ascii_chars = []
    ords = [ord(ch) for ch in data]

    # TODO: can set this based on your terminal width
    chunk_size = 32

    for i in range(0, len(data), chunk_size):
        ords_chunk = ords[i:i + chunk_size]
        for ch, ord_ in zip(data[i:i + chunk_size], ords_chunk):
            len_ord = len(str(ord_))
            print(ch.ljust(len_ord), end=' ')
        print()
        print(*ords_chunk)



    # for ch, ord_ in zip(data, ords):
    #     len_ord = len(str(ord_))
    #     print(ch.ljust(len_ord), end=' ')
    # print()
    # print(*ords)


    #for ch in data:
    #    chars.append(ch)
    #    ascii_chars.append(str(ord(ch)))
    #print(len(chars), len(ascii_chars))
    #print(chars)
    #print(ascii_chars)

    print("\n"+"="*64)

def win32_get_clipboard_data():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def win32_set_clipboard_data(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def win32_clean_clipboard_data(data, debug=True):
    if debug: char_to_ascii_print(data)
    new_data = ""
    for ch in data:
        #if(ord(ch) != 10 or ord(ch) != 13):
        ascii_val = ord(ch)
        if(ascii_val > 31 and ascii_val < 127):
            new_data += ch
        else:
            if ascii_val == 13:
                new_data += " "
    if debug: char_to_ascii_print(new_data)
    return new_data



def main():
    win32clipboard.OpenClipboard()
    #keyboard.add_hotkey('ctrl+shift+l', double_click_copy) 
    #keyboard.wait()
    #data = win32_get_clipboard_data()
    data = win32clipboard.GetClipboardData()
    
    print(data)
    new_data = win32_clean_clipboard_data(data)
    print(new_data)
    #win32_set_clipboard_data(data)
    #win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(new_data)  # I dont think this is working for some reason so call the other funciton below. 
    
    win32clipboard.CloseClipboard()
    #time.sleep(3)
    #input("wait")
    pyperclip.copy(new_data)



if __name__ == "__main__":
    main()