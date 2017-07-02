import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import purple, PCMYKColor, black, pink, green, blue
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Table, LongTable, TableStyle
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import LineLegend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis, AdjYValueAxis, NormalDateXValueAxis
from django.conf import settings
import datetime


def userPDF(myCanvas, resultsbuffer):
    # Target pdf file
    drawreportcover(myCanvas, resultsbuffer)
    drawsystemdailyefficiency(myCanvas, resultsbuffer)
    drawsystemefficiency(myCanvas, resultsbuffer)
    drawsystempeakefficieny(myCanvas, resultsbuffer)
    drawrelationshipcs(myCanvas, resultsbuffer)
    myCanvas.save()


"""
drawreportcover draws the cover page of the report
"""
def drawreportcover(can, resultsbuffer):
    width, height = A4
    logo_path = os.path.join(settings.BASE_DIR, 'Storage/static/Storage/images/kaer.jpg')
    can.drawImage(logo_path, 0, 690, width=width, height=2*inch, mask='auto')

    # define a large font
    can.setFont("Helvetica", 28)
    pdf_title = "Chiller Plants Operating Information Report"
    pdf_building_name = "for " + str(resultsbuffer).upper()
    can.drawString(25, 550, pdf_title)
    can.drawString(200, 500, pdf_building_name)

    can.setFont("Helvetica", 18)
    pdf_time = "Time generated: " + str(datetime.date.today())
    can.drawString(160, 400, pdf_time)

    pdf_copyright = "All right reserved by Kaer Pte Ltd"
    can.setFont("Helvetica", 20)
    can.drawString(150, 100, pdf_copyright)
    can.showPage()


"""
drawsystemdailyefficiency draws the system efficiency for a series of days indicated by administrators
or by default
"""
def drawsystemdailyefficiency(can, resultsbuffer):
    can.setFont("Helvetica", 24)
    sec_title = "Chiller Plant System Daily Efficiency"
    can.drawString(25, 750, sec_title)

    desc_text = "The chiller plant system daily efficiency demonstrates the total efficiency including every" \
                " parts of the system across a series of days. The range can be by default (say, 2 days) or" \
                " specified by administrators."
    stylesheet = getSampleStyleSheet()
    paragraph = Paragraph(desc_text, stylesheet['Normal'])
    aW, aH = 500, 600
    w, h = paragraph.wrap(aW, aH)
    if w <= aW and h <= aH:
        paragraph.drawOn(can, 25, 700)

    # Draw the chart
    drawing = Drawing(600, 400)

    # font
    fontName = 'Helvetica'
    fontSize = 7

    # chart
    lp = LinePlot()
    lp.y = 16
    lp.x = 32
    lp.width = 400
    lp.height = 200

    # line styles
    lp.lines.strokeWidth = 0
    lp.lines.symbol = makeMarker('FilledSquare')

    # x axis
    lp.xValueAxis = NormalDateXValueAxis()
    lp.xValueAxis.labels.fontName = fontName
    lp.xValueAxis.labels.fontSize = fontSize - 1
    lp.xValueAxis.forceEndDate = 1
    lp.xValueAxis.forceFirstDate = 1
    lp.xValueAxis.labels.boxAnchor = 'autox'
    lp.xValueAxis.xLabelFormat = '{d}-{MMM}'
    lp.xValueAxis.maximumTicks = 5
    lp.xValueAxis.minimumTickSpacing = 0.5
    lp.xValueAxis.niceMonth = 0
    lp.xValueAxis.strokeWidth = 1
    lp.xValueAxis.loLLen = 5
    lp.xValueAxis.hiLLen = 5
    lp.xValueAxis.gridEnd = drawing.width
    lp.xValueAxis.gridStart = lp.x - 10

    # y axis
    # self.chart.yValueAxis = AdjYValueAxis()
    lp.yValueAxis.visibleGrid = 1
    lp.yValueAxis.visibleAxis = 0
    lp.yValueAxis.labels.fontName = fontName
    lp.yValueAxis.labels.fontSize = fontSize - 1
    lp.yValueAxis.labelTextFormat = '%0.2f%%'
    lp.yValueAxis.strokeWidth = 0.25
    lp.yValueAxis.visible = 1
    lp.yValueAxis.labels.rightPadding = 5

    # self.chart.yValueAxis.maximumTicks = 6
    lp.yValueAxis.rangeRound = 'both'
    lp.yValueAxis.tickLeft = 7.5
    lp.yValueAxis.minimumTickSpacing = 0.5
    lp.yValueAxis.maximumTicks = 8
    lp.yValueAxis.forceZero = 0
    lp.yValueAxis.avoidBoundFrac = 0.1

    # legend
    ll = LineLegend()
    ll.fontName = fontName
    ll.fontSize = fontSize
    ll.alignment = 'right'
    ll.dx = 5

    # sample data
    lp.data = [
        [(19010706, 3.3900000000000001), (19010806, 3.29), (19010906, 3.2999999999999998), (19011006, 3.29),
         (19011106, 3.3399999999999999), (19011206, 3.4100000000000001), (19020107, 3.3700000000000001),
         (19020207, 3.3700000000000001), (19020307, 3.3700000000000001), (19020407, 3.5),
         (19020507, 3.6200000000000001), (19020607, 3.46), (19020707, 3.3900000000000001)],
        [(19010706, 3.2000000000000002), (19010806, 3.1200000000000001), (19010906, 3.1400000000000001),
         (19011006, 3.1400000000000001), (19011106, 3.1699999999999999), (19011206, 3.23),
         (19020107, 3.1899999999999999), (19020207, 3.2000000000000002), (19020307, 3.1899999999999999),
         (19020407, 3.3100000000000001), (19020507, 3.4300000000000002), (19020607, 3.29),
         (19020707, 3.2200000000000002)]]

    lp.lines[0].strokeColor = PCMYKColor(0, 100, 100, 40, alpha=100)
    lp.lines[1].strokeColor = PCMYKColor(100, 0, 90, 50, alpha=100)
    lp.xValueAxis.strokeColor = PCMYKColor(100, 60, 0, 50, alpha=100)
    ll.colorNamePairs = [(PCMYKColor(0, 100, 100, 40, alpha=100), '01-Mar-2017'),
                         (PCMYKColor(100, 0, 90, 50, alpha=100), '02-Mar-2017')]
    lp.lines.symbol.x = 0
    lp.lines.symbol.strokeWidth = 0
    lp.lines.symbol.arrowBarbDx = 5
    lp.lines.symbol.strokeColor = PCMYKColor(0, 0, 0, 0, alpha=100)
    lp.lines.symbol.fillColor = None
    lp.lines.symbol.arrowHeight = 5
    ll.dxTextSpace = 7
    ll.boxAnchor = 'nw'
    ll.subCols.dx = 0
    ll.subCols.dy = -2
    ll.subCols.rpad = 0
    ll.columnMaximum = 1
    ll.deltax = 1
    ll.deltay = 0
    ll.dy = 5
    ll.y = 240
    ll.x = 300
    lp.lines.symbol.kind = 'FilledCross'
    lp.lines.symbol.size = 5
    lp.lines.symbol.angle = 45

    drawing.add(lp)
    drawing.add(ll)
    # drawing.title.text = "Jurong Point System Efficiency"
    # drawing.title.fondSize = 16
    drawing.drawOn(can, 100, 450)

    can.showPage()


"""
drawsystemefficiency draws the system efficiency breakdown for different parts of the system
"""
def drawsystemefficiency(can, resultsbuffer):
    can.setFont("Helvetica", 24)
    sec_title = "System Efficiency Breakdown"
    can.drawString(25, 750, sec_title)

    desc_text = "The system operating efficiency consists of the metrics of different parts" \
                "in the system: chillers, chilled water pumps, condenser water pumps and cooling" \
                "towers. Here we demonstrate the average efficiency measured for each day from () " \
                "to ()."
    stylesheet = getSampleStyleSheet()
    paragraph = Paragraph(desc_text, stylesheet['Normal'])
    aW, aH = 500, 600
    w, h = paragraph.wrap(aW, aH)
    if w <= aW and h <= aH:
        paragraph.drawOn(can, 25, 700)

    chiller_efficiency = Paragraph("Chiller Efficiency", stylesheet['Normal'])
    chwp_efficiency = Paragraph("Chilled Water Pump Efficiency", stylesheet['Normal'])
    cwp_efficiency = Paragraph("Condenser Water Pump Efficiency", stylesheet['Normal'])
    ct_efficiency = Paragraph("Cooling Tower Efficiency", stylesheet['Normal'])
    overall_efficiency = Paragraph("Overall Efficiency", stylesheet['Normal'])
    data = [[' ', '1st Day', '2nd Day', '3rd Day', 'unit'],
            [chiller_efficiency, '0.712', '0.734', '0.723', 'KW/RT'],
            [chwp_efficiency, '0.043', '0.076', '0.034', 'KW/RT'],
            [cwp_efficiency, '0.040', '0.041', '0.042', 'KW/RT'],
            [ct_efficiency, '0.029', '0.021', '0.023', 'KW/RT'],
            [overall_efficiency, '0.784', '0.831', '0.780', 'KW/RT']]
    t = Table(data, 5 * [1 * inch], 6 * [1 * inch])
    t.setStyle(TableStyle([('TEXTCOLOR', (1, 1), (-2, -1), colors.red),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('TEXTCOLOR', (0, -1), (0, -1), colors.green),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))
    t.wrapOn(can, 500, 500)
    t.drawOn(can, 100, 250)
    can.showPage()


"""
drawsystempeakefficiency shows the peak efficiency value for each part of the system
spanning across a certain time (day or few days)
"""
def drawsystempeakefficieny(can, resultsbuffer):
    can.setFont("Helvetica", 24)
    sec_title = "System Peak Efficiency Breakdown"
    can.drawString(25, 750, sec_title)

    desc_text = "The system operating peak efficiency measures the peak efficiency value between " \
                "the selected dates for different parts of the system."
    stylesheet = getSampleStyleSheet()
    paragraph = Paragraph(desc_text, stylesheet['Normal'])
    aW, aH = 500, 600
    w, h = paragraph.wrap(aW, aH)
    if w <= aW and h <= aH:
        paragraph.drawOn(can, 25, 700)

    peak = (ce_peak, chwp_peak, cwp_peak, ct_peak) = (0.656, 0.075, 0.024, 0.027)
    overall_peak = sum(peak)
    chiller_peak_str = Paragraph("Chiller Efficiency", stylesheet['Normal'])
    chwp_peak_str = Paragraph("Chilled Water Pump Efficiency", stylesheet['Normal'])
    cwp_peak_str = Paragraph("Condenser Water Pump Efficiency", stylesheet['Normal'])
    ct_peak_str = Paragraph("Cooling Tower Efficiency", stylesheet['Normal'])
    overall_peak_str = Paragraph("Overall Efficiency", stylesheet['Normal'])
    data = [[' ', 'Peak', 'Unit'],
            [chiller_peak_str, ce_peak, 'KW/RT'],
            [chwp_peak_str, chwp_peak, 'KW/RT'],
            [cwp_peak_str, cwp_peak, 'KW/RT'],
            [ct_peak_str, ct_peak, 'KW/RT'],
            [overall_peak_str, overall_peak, 'KW/RT']]
    t = Table(data, [2.5 * inch, inch, inch], 6 * [0.5 * inch])
    t.setStyle(TableStyle([('TEXTCOLOR', (1, 1), (-2, -1), colors.red),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('TEXTCOLOR', (0, -1), (0, -1), colors.green),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))
    t.wrapOn(can, 500, 500)
    t.drawOn(can, 100, 450)

    can.showPage()


"""
drawheatbalance shows the relationship between cooling load (c) and system efficiency (s)
"""
def drawrelationshipcs(can, resultsbuffer):
    can.setFont("Helvetica", 24)
    sec_title = "System Heat Balance"
    can.drawString(25, 750, sec_title)

    desc_text = "The following figure shows the relationship between the chilled water" \
                " system operating efficiency and the cooling load. As the figure shows, with " \
                "the Cooling load ranges between 800 RT to 1100 RT, the efficiency hovers between " \
                "0.75/RT to 0.91KW/RT."
    stylesheet = getSampleStyleSheet()
    paragraph = Paragraph(desc_text, stylesheet['Normal'])
    aW, aH = 500, 600
    w, h = paragraph.wrap(aW, aH)
    if w <= aW and h <= aH:
        paragraph.drawOn(can, 25, 700)

    drawing = Drawing(600, 400)
    data = [
        ((801, 0.7), (903, 0.8), (799, 0.84), (1002, 0.97), (1101, 0.89)),
        ((987, 0.98), (1007, 1.1), (1102, 0.98), (987, 0.95), (908, 0.89))
    ]
    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 250
    lp.width = 400
    lp.data = data
    lp.joinedLines = 0
    lp.lines.symbol = makeMarker('FilledCircle')
    # lp.lines.symbol = makeMarker('Circle')
    # lp.lines[1].symbol = makeMarker('Circle')
    lp.lineLabelFormat = '%2.0f'
    lp.strokeColor = colors.black
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = 1200
    lp.xValueAxis.valueSteps = [0.00, 200.00, 400.00, 600.00, 800.00, 1000.00, 1200.00]
    lp.xValueAxis.labelTextFormat = '%2.1f'
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 1.2
    lp.yValueAxis.valueSteps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    drawing.add(lp)
    drawing.drawOn(can, 50, 350)

    can.showPage()