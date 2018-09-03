'Looking through stock market data and summarize
'Ticker, yearly change, percent change, total volume of stock

Sub stock_summary()

'set initial values for first ticker to start algorithm
ticker = Cells(2, 1).Value
start_stock_value = Cells(2, 3).Value
total_stock_volume = 0

'determine how long for loop must run by setting end row of raw data
end_raw_row = Range("A1",Range("A1").End(xlDown)).Rows.Count

'set location of summary data and name headers and format them
Cells(1,9).Value = "Ticker"
Cells(1,10).Value = "Yearly Change"
Cells(1,11).Value = "Perecent Change"
Cells(1,12).Value = "Total Stock Volume"
Range(Cells(1, 9), Cells(1, 12)).Font.Bold = True
Range(Cells(1, 9), Cells(1, 12)).WrapText = True
summary_row = 2

'freeze top row so that easier to look through data with headings always showing
Rows("2:2").Select
ActiveWindow.FreezePanes = True


For i = 2 To end_raw_row
   
    current_row_ticker = Cells(i, 1).Value
    next_row_ticker = Cells(i + 1, 1).Value
      
    If current_row_ticker = next_row_ticker Then
        total_stock_volume = total_stock_volume + Cells(i, 7).Value
       
    ElseIf current_row_ticker <> next_row_ticker Then
        total_stock_volume = total_stock_volume + Cells(i, 7).Value
        end_stock_value = Cells(i, 6).Value
        yearly_change = end_stock_value - start_stock_value 
        percent_change = yearly_change/start_stock_value

        'print out stock values to the summary table
        Cells(summary_row, 9).Value = ticker
        Cells(summary_row, 10).Value = yearly_change
        If yearly_change > 0 Then
            Cells(summary_row, 10).Interior.ColorIndex = 4
        Else 
            Cells(summary_row, 10).Interior.ColorIndex = 3
        End If
        Cells(summary_row, 11).Value = percent_change
        Cells(summary_row, 11).NumberFormat = "0.00%"
        Cells(summary_row, 12).Value = total_stock_volume
        
        'reset values for next stock 
        ticker = Cells(i+1, 1).Value
        start_stock_value = Cells(i+1, 3).Value
        total_stock_volume = 0

        'iterate next summary table rwo location
        summary_row = summary_row + 1

    End If

Next i

End Sub