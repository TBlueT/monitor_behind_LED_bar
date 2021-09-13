import win32api, win32con, win32gui, win32ui
import time, threading


class DIs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.windowText = "0"
        self.writeWindow = True
        self.hWindow = [None]

    def windowText_intput(self, input):
        self.windowText = input
        self.customDraw(self.hWindow)

    def run(self):

        hInstance = win32api.GetModuleHandle()

        className = 'RGB LED Light'

        wndClass                = win32gui.WNDCLASS()

        wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className

        wndClassAtom = win32gui.RegisterClass(wndClass)

        exStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

        style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

        self.hWindow = win32gui.CreateWindowEx(
            exStyle,
            wndClassAtom,
            None, # WindowName
            style,
            int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/30)*29, # x
            0, # y
            int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/30), # width
            int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)/20), # height
            None, # hWndParent
            None, # hMenu
            hInstance,
            None # lpParam
        )

        win32gui.SetLayeredWindowAttributes(self.hWindow, win32api.RGB(255,255,255), 200, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)

        win32gui.SetWindowPos(self.hWindow, win32con.HWND_TOP, 0, 0, 0, 0,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW)

        win32gui.UpdateWindow(self.hWindow)

        win32gui.PumpMessages()

    def customDraw(self, hWindow):
        global windowText

        windowText = self.windowText
        win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)


    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hWnd)

            dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
            fontSize = 50

            lf = win32gui.LOGFONT()
            lf.lfFaceName = "Times New Roman"
            lf.lfHeight = int(round(dpiScale * fontSize))

            hf = win32gui.CreateFontIndirect(lf)
            win32gui.SelectObject(hdc, hf)

            rect = win32gui.GetClientRect(hWnd)
            win32gui.SetTextColor(hdc, win32api.RGB(0,255,0))
            win32gui.DrawText(
                hdc,
                self.windowText,
                -1,
                rect,
                win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER | win32con.DT_RIGHT
            )

            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        elif message == win32con.WM_DESTROY:
            print('Closing the window.')
            win32gui.PostQuitMessage(0)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

