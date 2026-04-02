import tkinter as tk
import webbrowser
import os



BarWidth = 600
BarHeight = 50
BarRadius = 25
BgColour = "#303134"
BorderColour = "#5F6368"
BorderHoverColour = "#8AB4F8"
TextColour = "#E8EAED"
PlaceholderColour = "#9AA0A6"
AccentColour = "#8AB4F8"
IconColour = "#9AA0A6"
FontFamily = "Segoe UI"
FontSize = 13
GoogleSearchUrl = "https://www.google.com/search?q="
SnapThreshold = 40
PositionFile = os.path.join(os.path.expanduser("~"), "SearchPosition.txt")


def LoadPosition(ScreenWidth: int, ScreenHeight: int) -> tuple:
    try:
        with open(PositionFile, "r") as F:
            Parts = F.read().strip().split(",")
            return int(Parts[0]), int(Parts[1])
    except Exception:
        return (ScreenWidth - BarWidth) // 2, ScreenHeight - 100


def SavePosition(X: int, Y: int) -> None:
    try:
        with open(PositionFile, "w") as F:
            F.write(f"{X},{Y}")
    except Exception:
        pass


def SnapPosition(X: int, Y: int, ScreenWidth: int, ScreenHeight: int) -> tuple:
    CenterX = (ScreenWidth - BarWidth) // 2
    CenterY = (ScreenHeight - BarHeight) // 2
    SnappedX = CenterX if abs(X - CenterX) < SnapThreshold else X
    SnappedY = CenterY if abs(Y - CenterY) < SnapThreshold else Y
    return SnappedX, SnappedY


def DrawBar(Canvas: tk.Canvas, Hovered: bool = False) -> None:
    Canvas.delete("all")
    R = BarRadius
    W = BarWidth
    H = BarHeight
    Border = BorderHoverColour if Hovered else BorderColour

    Canvas.create_arc(0, 0, R * 2, R * 2, start=90, extent=90, fill=BgColour, outline=BgColour)
    Canvas.create_arc(W - R * 2, 0, W, R * 2, start=0, extent=90, fill=BgColour, outline=BgColour)
    Canvas.create_arc(0, H - R * 2, R * 2, H, start=180, extent=90, fill=BgColour, outline=BgColour)
    Canvas.create_arc(W - R * 2, H - R * 2, W, H, start=270, extent=90, fill=BgColour, outline=BgColour)
    Canvas.create_rectangle(R, 0, W - R, H, fill=BgColour, outline=BgColour)
    Canvas.create_rectangle(0, R, W, H - R, fill=BgColour, outline=BgColour)

    Canvas.create_arc(1, 1, R * 2 + 1, R * 2 + 1, start=90, extent=90, style="arc", outline=Border)
    Canvas.create_arc(W - R * 2 - 1, 1, W - 1, R * 2 + 1, start=0, extent=90, style="arc", outline=Border)
    Canvas.create_arc(1, H - R * 2 - 1, R * 2 + 1, H - 1, start=180, extent=90, style="arc", outline=Border)
    Canvas.create_arc(W - R * 2 - 1, H - R * 2 - 1, W - 1, H - 1, start=270, extent=90, style="arc", outline=Border)
    Canvas.create_line(R, 1, W - R, 1, fill=Border)
    Canvas.create_line(R, H - 1, W - R, H - 1, fill=Border)
    Canvas.create_line(1, R, 1, H - R, fill=Border)
    Canvas.create_line(W - 1, R, W - 1, H - R, fill=Border)

    Cx = 25
    Cy = H // 2
    Sr = 9
    Canvas.create_oval(Cx - Sr, Cy - Sr, Cx + Sr, Cy + Sr, outline=IconColour, width=1.5)
    Canvas.create_line(Cx + Sr - 1, Cy + Sr - 1, Cx + Sr + 5, Cy + Sr + 5,
                       fill=IconColour, width=3, capstyle="round")


def BuildWindow() -> None:
    Root = tk.Tk()
    Root.overrideredirect(True)
    Root.attributes("-topmost", False)
    Root.wm_attributes("-transparentcolor", "magenta")
    Root.config(bg="magenta")

    ScreenWidth = Root.winfo_screenwidth()
    ScreenHeight = Root.winfo_screenheight()
    StartX, StartY = LoadPosition(ScreenWidth, ScreenHeight)
    Root.geometry(f"{BarWidth}x{BarHeight}+{StartX}+{StartY}")

    Canvas = tk.Canvas(
        Root,
        width=BarWidth,
        height=BarHeight,
        bg="magenta",
        highlightthickness=0,
        bd=0
    )
    Canvas.place(x=0, y=0)
    DrawBar(Canvas, Hovered=False)

    EntryX = 45
    EntryW = BarWidth - EntryX - 40
    SearchEntry = tk.Entry(
        Root,
        font=(FontFamily, FontSize),
        fg=PlaceholderColour,
        bg=BgColour,
        insertbackground=AccentColour,
        bd=0,
        highlightthickness=0,
        relief="flat"
    )
    SearchEntry.insert(0, "Search...")
    SearchEntry.place(x=EntryX, y=(BarHeight - 20) // 2, width=EntryW, height=20)

    CloseCanvas = tk.Canvas(
        Root,
        width=20,
        height=20,
        bg=BgColour,
        highlightthickness=0,
        bd=0,
        cursor="hand2"
    )
    CloseCanvas.place(x=BarWidth - 30, y=(BarHeight - 20) // 2)

    def DrawClose(Hovered: bool = False) -> None:
        CloseCanvas.delete("all")
        Colour = TextColour if Hovered else PlaceholderColour
        CloseCanvas.create_line(5, 5, 15, 15, fill=Colour, width=1.5, capstyle="round")
        CloseCanvas.create_line(15, 5, 5, 15, fill=Colour, width=1.5, capstyle="round")

    DrawClose(False)

    def OnCloseEnter(Event) -> None:
        DrawClose(True)
        DrawBar(Canvas, True)

    def OnCloseLeave(Event) -> None:
        DrawClose(False)
        DrawBar(Canvas, False)

    def OnCloseClick(Event) -> None:
        SavePosition(Root.winfo_x(), Root.winfo_y())
        Root.destroy()

    CloseCanvas.bind("<Enter>", OnCloseEnter)
    CloseCanvas.bind("<Leave>", OnCloseLeave)
    CloseCanvas.bind("<Button-1>", OnCloseClick)

    def OnFocusIn(Event) -> None:
        if SearchEntry.get() == "Search...":
            SearchEntry.delete(0, tk.END)
            SearchEntry.config(fg=TextColour)
        DrawBar(Canvas, Hovered=True)

    def OnFocusOut(Event) -> None:
        if not SearchEntry.get():
            SearchEntry.insert(0, "Search...")
            SearchEntry.config(fg=PlaceholderColour)
        DrawBar(Canvas, Hovered=False)

    def OnEnter(Event) -> None:
        Query = SearchEntry.get().strip()
        if Query and Query != "Search...":
            webbrowser.open(GoogleSearchUrl + Query.replace(" ", "+"))

    SearchEntry.bind("<FocusIn>", OnFocusIn)
    SearchEntry.bind("<FocusOut>", OnFocusOut)
    SearchEntry.bind("<Return>", OnEnter)

    DragData = {"X": 0, "Y": 0, "Dragging": False}

    def OnDragStart(Event) -> None:
        DragData["X"] = Event.x_root - Root.winfo_x()
        DragData["Y"] = Event.y_root - Root.winfo_y()
        DragData["Dragging"] = True

    def OnDrag(Event) -> None:
        if not DragData["Dragging"]:
            return
        NewX = Event.x_root - DragData["X"]
        NewY = Event.y_root - DragData["Y"]
        Root.geometry(f"+{NewX}+{NewY}")

    def OnDragEnd(Event) -> None:
        DragData["Dragging"] = False
        RawX = Root.winfo_x()
        RawY = Root.winfo_y()
        FinalX, FinalY = SnapPosition(RawX, RawY, ScreenWidth, ScreenHeight)
        if FinalX != RawX or FinalY != RawY:
            Root.geometry(f"+{FinalX}+{FinalY}")
        SavePosition(FinalX, FinalY)

    Canvas.bind("<ButtonPress-1>", OnDragStart)
    Canvas.bind("<B1-Motion>", OnDrag)
    Canvas.bind("<ButtonRelease-1>", OnDragEnd)

    Root.mainloop()


if __name__ == "__main__":
    BuildWindow()



