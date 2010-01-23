class BppEnum:
    _4BPP_CGA  = 1
    _6BPP_NES  = 2
    _8BPP_EGA  = 3
    _9BPP_RGB  = 4
    _15BPP_RGB = 5
    _16BPP_RGB = 6
    _24BPP_RGB = 7
    _32BPP_ARGB = 8
    
class Tool:
    SELECT = 10
    MOVE_SELECTION = 11
    COLOR_SELECTOR = 12
    PENCIL = 13
    LINE = 14
    FLOODFILL = 15
    COLOR_REPLACE = 16

class Movement: 
    ShiftLeft    = 100
    ShiftRight   = 101
    ShiftUp      = 102
    ShiftDown    = 103
    PageUp       = 104
    PageDown     = 105
    RowBackward  = 106
    RowForward   = 107
    TileBackward = 108
    TileForward  = 109
    ByteBackward = 110
    ByteForward  = 111
    