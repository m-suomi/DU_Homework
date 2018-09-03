'Runs the stock summary for every worksheet in a file
Sub run_stocks()
    For Each ws In Worksheets
        ws.Activate 'activates the next sheet so all cell references are within the current sheet
        stock_summary 'runs stock summary function
    Next ws
End Sub


'For one sheet, looking through stock market data and summarize
'Ticker, yearly change, percent change, total volume of stock
'And then for hard section determining the largerst changes and volume of all stock

Sub stock_summary()

'set initial values for first ticker to start algorithm
ticker = Cells(2, 1).Value
start_stock_value = Cells(2, 3).Value
total_stock_volume = 0

'set initial values for summary of max/min stock prices
greatest_percent_increase = 0
greatest_percent_increase_ticker = ""
greatest_percent_decrease = 0
greatest_percent_decrease_ticker = ""
greatest_total_volume = 0
greatest_total_volume_ticker = ""

'determine how long for loop must run by setting end row of raw data
end_raw_row = Range("A1",Range("A1").End(xlDown)).Rows.Count

'set location of summary data and name headers and format them
Cells(1,9).Value = "Ticker"
Cells(1,10).Value = "Yearly Change"
Cells(1,11).Value = "Percent Change"
Cells(1,12).Value = "Total Stock Volume"
Cells(1,16).Value = "Ticker"
Cells(1,17).Value = "Value"
Range(Cells(1, 9), Cells(1, 17)).Font.Bold = True
Range(Cells(1, 9), Cells(1, 17)).WrapText = True
Cells(2,15).Value = "Greatest % Increase"
Cells(3,15).Value = "Greatest % Decrease"
Cells(4,15).Value = "Greatest Total Volume"
Range(Cells(2, 15), Cells(4, 15)).Font.Bold = True
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
        'perform final calculations for this stock
        total_stock_volume = total_stock_volume + Cells(i, 7).Value
        end_stock_value = Cells(i, 6).Value
        yearly_change = end_stock_value - start_stock_value 
        'need to add in this If function for stocks that have zero values in them
        'so that it doesn't divide by zero and stop the script because it is getting infinity
        'not sure why some of the data has zeros, but need to deal with it        
        If start_stock_value = 0 Then
            percent_change = 0
        Else
            percent_change = yearly_change/start_stock_value
        End If
        
        'print out stock values to the summary table and update formatting
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
        
        'check/update greatest volume, %inc, %dec
        If percent_change > greatest_percent_increase Then
            greatest_percent_increase_ticker = ticker
            greatest_percent_increase = percent_change
        ElseIf percent_change < greatest_percent_decrease Then
            greatest_percent_decrease_ticker = ticker
            greatest_percent_decrease = percent_change
        End If

        If total_stock_volume > greatest_total_volume Then
            greatest_total_volume_ticker = ticker
            greatest_total_volume = total_stock_volume
        End If
            
        'reset values for next stock 
        ticker = Cells(i+1, 1).Value
        start_stock_value = Cells(i+1, 3).Value
        total_stock_volume = 0

        'iterate next summary table row location
        summary_row = summary_row + 1

    End If

Next i

'Print final greatest volume, %inc, %dec results
Cells(2,16).Value = greatest_percent_increase_ticker
Cells(2,17).Value = greatest_percent_increase
Cells(2,17).NumberFormat = "0.00%"
Cells(3,16).Value = greatest_percent_decrease_ticker
Cells(3,17).Value = greatest_percent_decrease
Cells(3,17).NumberFormat = "0.00%"
Cells(4,16).Value = greatest_total_volume_ticker
Cells(4,17).Value = greatest_total_volume
'Autofit column width, so greatest colum labels aren't hidden
Columns("O:O").Select
Selection.EntireColumn.AutoFit

End Sub