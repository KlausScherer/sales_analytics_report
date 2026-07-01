Attribute VB_Name = "Módulo1"
Sub FormatoTablaProductos()
Attribute FormatoTablaProductos.VB_Description = "Macro para dar formato a tabla de productos"
Attribute FormatoTablaProductos.VB_ProcData.VB_Invoke_Func = " \n14"
'
' FormatoTablaProductos Macro
' Macro para dar formato a tabla de productos
'

'
    Range("A1").Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.TextToColumns Destination:=Range("A1"), DataType:=xlDelimited, _
        TextQualifier:=xlDoubleQuote, ConsecutiveDelimiter:=False, Tab:=True, _
        Semicolon:=False, Comma:=True, Space:=False, Other:=False, FieldInfo _
        :=Array(Array(1, 1), Array(2, 1), Array(3, 1), Array(4, 1), Array(5, 1)), _
        TrailingMinusNumbers:=True
    Range("A1").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    With Selection.Font
        .Name = "Arial"
        .Size = 11
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ThemeColor = xlThemeColorLight1
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    Selection.Font.Size = 12
    Selection.Font.Bold = True
    With Selection
        .HorizontalAlignment = xlGeneral
        .VerticalAlignment = xlCenter
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlContext
        .MergeCells = False
    End With
    With Selection
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlContext
        .MergeCells = False
    End With
    Columns("A:A").Select
    Columns("A:A").EntireColumn.AutoFit
    Columns("B:B").Select
    Columns("B:B").EntireColumn.AutoFit
    Columns("C:C").Select
    Columns("C:C").EntireColumn.AutoFit
    Columns("D:D").Select
    Columns("D:D").EntireColumn.AutoFit
    Columns("E:E").Select
    Columns("E:E").EntireColumn.AutoFit
    Range("D2").Select
    ActiveCell.FormulaR1C1 = "Materiales de construcción"
    Range("D2").Select
    Selection.AutoFill Destination:=Range("D2:D9")
    Range("D2:D9").Select
    Range("A1:E1").Select
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent3
        .TintAndShade = 0.799981688894314
        .PatternTintAndShade = 0
    End With
    Range("A1").Select
End Sub
