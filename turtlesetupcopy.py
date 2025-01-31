# @title Setup Turtle

# Module for drawing classic Turtle figures on Google Colab notebooks.
# It uses HTML capabilities of IPython to draw SVG shapes inline.

from IPython.display import display, HTML, Javascript, clear_output
import time
import json
import math
import random
import colorsys

# -------------------------------------------------------------------------------------------------------
# JavaScript and HTML for the output canvas
# -------------------------------------------------------------------------------------------------------
createCanvas = '''
<style>
table {border-collapse: collapse;}
button {width: 80px; margin: 5px 5px 5px 0px; text-align: center; font-size: 1em;}
canvas {margin-top: 5px;}
#status {background-color: #cdcdff; color: #000000; font-size: 1em;}
#art {text-align: center; background-color: #efefff; padding: 0px 5px 0px 5px;}
.right {text-align: right;}
.left {text-align: left;}
.numbers {margin: 0px 10px 0px 10px; font-size: 1em; color: 'purple';
white-space: pre; font-family: 'Courier New', monospace;}
</style>
<table>
<tr><td colspan=4 id='art'><canvas id="turtleCanvas"></td></tr>
<tr id="status">
  <td class="left">
    <div id="info">
      <div class="numbers"><b>Turtle</b> - Waiting ..                </div>
    </div>
  </td>
  <td class="left">
    <div id="coord">
      <div class='numbers'><b>Mouse</b> - x:   0 y:   0</div>
    </div>
  </td>
  <td class="right">
    <button onClick="replay();" id="replay">Replay</button>
    <button onClick="saveImg();" id="save">Save</button>
  </td>
</tr>
</table>
<script>
function saveImg() {
  var a = document.createElement("a");
  a.download = "turtle.png"; a.href = c.toDataURL("image/png"); a.click();
}
function replay() {
  var t=Math.max(Math.round(2000/p.length), 1);
  disableControls(true);
  setTimeout(function() { play(t); }, 50);
}
function disableControls(disable) {
  document.getElementById("replay").disabled = disable;
  document.getElementById("save").disabled = disable;
}
function play(delay) {
  clearCanvas(bgcolor);
  cold = ctx.getImageData(0, 0, c.width, c.height);
  if(delay > 0) {
    (function myLoop(i) {
      setTimeout(function() {
        plot(i, delay);
        if (++i < p.length) { myLoop(i); } else { disableControls(false); }
      }, delay)
    })(1);
  } else {
    for (var ip=1; ip<p.length; ip++) { plot(ip, delay); }
    disableControls(false);
  }
}
function plot(ip, delay) {
  if(dirty) { ctx.putImageData(cold, 0, 0); }
  if(p[ip-1].fill!=p[ip].fill   || p[ip-1].width!=p[ip].width ||
     p[ip-1].color!=p[ip].color || p[ip-1].fillcolor!=p[ip].fillcolor ||
     ip==1) {
    if(p[ip-1].fill) {
      ctx.fillStyle = p[ip-1].fillcolor;
      ctx.fill();
    }
    ctx.beginPath();
    ctx.moveTo(p[ip-1].x, p[ip-1].y);
    ctx.strokeStyle = p[ip].color;
    ctx.lineWidth = p[ip].width;
  }
  if(p[ip].pen) { ctx.lineTo(p[ip].x, p[ip].y); }
  else          { ctx.moveTo(p[ip].x, p[ip].y); }
  ctx.stroke();
  if(turtle && (delay > 0 || ip==p.length-1)) { showTurtle(ip); }
  updateStatus(p[ip].x, p[ip].y, p[ip].h, ip);
}
function updateStatus(x,y,h,ip) {
  px=String(Math.round(x)).padStart(4,' ');
  py=String(Math.round(y)).padStart(4,' ');
  ph=String(Math.round(h)).padStart(4,' ');
  pi=String(ip).padStart(6,' ');
  document.getElementById("info").innerHTML=
  "<div class='numbers'><b>Turtle</b> - x:"+px+" y:"+py+
  " Heading:"+ph+" - Points:"+pi+"</div>";
}
function updateStatusStatic(ip) {
  pi=String(ip).padStart(6,' ');
  document.getElementById("info").innerHTML=
  "<div class='numbers'><b>Turtle</b> - Points:"+pi+
  " (non interactive)           </div>";
}
function getCoordinates(e) {
  var rect = c.getBoundingClientRect();
  mx=String(Math.round(e.clientX-rect.left)).padStart(4,' ');
  my=String(Math.round(e.clientY-rect.top)).padStart(4,' ');
  document.getElementById("coord").innerHTML=
  "<div class='numbers'><b>Mouse</b> - x:"+mx+" y:"+my+"</div>";
}
function showTurtle(ip) {
  cold = ctx.getImageData(0, 0, c.width, c.height);
  ctx.translate(p[ip].x, p[ip].y);
  ctx.rotate(p[ip].h*Math.PI/180.);
  ctx.drawImage(timg, -timg.width/2, -timg.height / 2, timg.width, timg.height);
  ctx.rotate(-p[ip].h*Math.PI/180.);
  ctx.translate(-p[ip].x, -p[ip].y);
  dirty = true;
}
function clearCanvas(color){
  bgcolor = color;
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, c.width, c.height);
}
function initTurtle() {
  var turl = "https://raw.githubusercontent.com/tproffen/ORCSGirlsPython/master/Images/turtle.png";
  timg = new Image();
  timg.src = turl; timg.setAttribute('crossorigin', 'anonymous');
}
//-----------------------------------------------------------------//
//----------- Functions called from Python ------------------------//
//-----------------------------------------------------------------//
function updateDrawingCanvas(json) {
  var art = JSON.parse(json);
  bgcolor = art.bgcolor;
  turtle = art.turtle;
  c.width = art.width; c.height = art.height;
  document.getElementById("art").style.backgroundColor  = art.canvascolor;
  document.getElementById("status").style.backgroundColor  = art.statuscolor;

  p=art.lines;
  disableControls(true);
  setTimeout(function() { play(art.delay); }, 50);
}
//-----------------------------------------------------------------//
function updateDrawingSVG(svg,np) {

  blob = new Blob([svg],{type:'image/svg+xml;charset=utf-8'});
  url = URL.createObjectURL(blob);
  var img = new Image();
  img.onload = function(e){
    c.width=img.width; c.height=img.height;
    ctx.drawImage( img, 0, 0 );
  };
  img.src = url;
  document.getElementById("save").disabled = false;
  updateStatusStatic(np);
}
//-----------------------------------------------------------------//
//-----------------------------------------------------------------//
var c = document.getElementById("turtleCanvas");
var ctx = c.getContext("2d");
var cold = ctx.getImageData(0, 0, c.width, c.height);
var p = [], timg, turtle = false; path = false; dirty = false;

initTurtle(); disableControls(true); c.addEventListener('mousemove',getCoordinates);
</script>
'''

# -------------------------------------------------------------------------------------------------------
# Turtle state and default values
# -------------------------------------------------------------------------------------------------------

defaultCanvas = {
    'bgcolor': 'white',
    'statuscolor': '#ededff',
    'turtle': False,
    'canvascolor': '#fafafa',
    'width': 1000,
    'height': 600,
    'delay': 0
}

defaultTurtle = {
    'pen': False,
    'x': 0,
    'y': 0,
    'h': 0,
    'color': 'blue',
    'width': 2,
    'fill': False,
    'fillcolor': 'yellow'
}

defaultDrawMode = 'auto'

# -------------------------------------------------------------------------------------------------------
# Internal functions
# -------------------------------------------------------------------------------------------------------

SVG_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="{window_width}" height="{window_height}">
  <rect width="100%" height="100%" fill="{background_color}"/>
  {groups}
</svg>
"""

SVG_GRP = """
<g fill="{fillcolor}">
  <path d="{points}" stroke="{pen_color}" stroke-width="{pen_width}"/>
</g>
"""

def _generateSVG():
    global currentCanvas

    curr = currentCanvas['lines'][0]
    last = len(currentCanvas['lines']) - 1
    points = ""
    groups = ""
    prev = currentCanvas['lines'][0]
    for k, p in enumerate(currentCanvas['lines']):
        if (p['color'] != curr['color'] or p['width'] != curr['width'] or
            p['fillcolor'] != curr['fillcolor'] or p['fill'] != curr['fill'] or
            k == last):

            fill = p['fillcolor'] if curr['fill'] else 'none'
            groups += SVG_GRP.format(
                fillcolor=fill,
                pen_color=curr['color'],
                pen_width=curr['width'],
                points=points
            )
            points = "M{} {} ".format(prev['x'], prev['y'])
            curr = p

        cmd = 'L' if p['pen'] else 'M'
        points += "{}{} {} ".format(cmd, p['x'], p['y'])
        prev = p

    svg = SVG_TEMPLATE.format(
        window_width=currentCanvas['width'],
        window_height=currentCanvas['height'],
        background_color=currentCanvas['bgcolor'],
        groups=groups
    )
    return svg

def _updateDrawing():
    global currentCanvas, drawing_window, drawing_mode
    if drawing_window is None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    lsvg = (drawing_mode == 'svg' or (drawing_mode == 'auto' and len(currentCanvas['lines']) > 2000))
    if lsvg:
        svg = _generateSVG()
        np = len(currentCanvas['lines'])
        cmd = 'updateDrawingSVG(`{}`,{})'.format(svg, np)
    else:
        jsondrawing = json.dumps(currentCanvas)
        cmd = 'updateDrawingCanvas(\'{}\')'.format(jsondrawing)
    drawing_window.update(HTML(createCanvas))
    display(Javascript(cmd))

def _updateTurtleXY(nx, ny, nh):
    global currentTurtle, currentCanvas
    currentTurtle['x'] = nx
    currentTurtle['y'] = ny
    currentTurtle['h'] = nh
    currentCanvas['lines'].append(currentTurtle.copy())

def _newHeading(x, y):
    global currentCanvas
    cind = len(currentCanvas['lines']) - 1
    h = math.degrees(math.atan2(x - currentCanvas['lines'][cind]['x'], currentCanvas['lines'][cind]['y'] - y))
    h = (h + 360) % 360
    return h

def getTurtleCanvas():
    global currentCanvas
    return currentCanvas

def saveSVG(file):
    with open(file, "w") as f:
        f.write(_generateSVG())

# -------------------------------------------------------------------------------------------------------
# Turtle functions
# -------------------------------------------------------------------------------------------------------

def initializeTurtle(initial_window_size=(1000, 600), mode='auto'):
    global defaultCanvas, defaultTurtle, currentCanvas, currentTurtle
    global drawing_window, drawing_mode

    clear_output(wait=True)
    drawing_mode = mode
    drawing_window = display(HTML(createCanvas), display_id=True)
    currentCanvas = defaultCanvas.copy()
    currentCanvas['width'], currentCanvas['height'] = initial_window_size
    currentCanvas['lines'] = []
    currentTurtle = defaultTurtle.copy()
    _updateTurtleXY(currentCanvas['width'] / 2, currentCanvas['height'] / 2, 0.0)

def forward(units):
    global currentCanvas, currentTurtle

    alpha = math.radians(currentTurtle['h'])
    cind = len(currentCanvas['lines']) - 1
    endx = currentCanvas['lines'][cind]['x'] + units * math.sin(alpha)
    endy = currentCanvas['lines'][cind]['y'] - units * math.cos(alpha)
    _updateTurtleXY(endx, endy, currentTurtle['h'])

def backward(units):
    forward(-units)

def setx(x):
    global currentTurtle
    newh = _newHeading(x, currentTurtle['y'])
    _updateTurtleXY(x, currentTurtle['y'], newh)

def sety(y):
    global currentTurtle
    newh = _newHeading(currentTurtle['x'], y)
    _updateTurtleXY(currentTurtle['x'], y, newh)

def goto(x, y):
    global currentTurtle
    newh = _newHeading(x, y)
    _updateTurtleXY(x, y, newh)

def jump(x, y):
    penup()
    _updateTurtleXY(x, y, currentTurtle['h'])
    pendown()

def getx():
    global currentTurtle
    return currentTurtle['x']

def gety():
    global currentTurtle
    return currentTurtle['y']

def heading():
    global currentTurtle
    return currentTurtle['h']

def face(degrees):
    global currentTurtle
    newheading = degrees % 360
    _updateTurtleXY(currentTurtle['x'], currentTurtle['y'], newheading)

def left(degrees):
    global currentTurtle
    newheading = (currentTurtle['h'] - degrees) % 360
    _updateTurtleXY(currentTurtle['x'], currentTurtle['y'], newheading)

def right(degrees):
    left(-degrees)

def penup():
    global currentTurtle
    currentTurtle['pen'] = False

def pendown():
    global currentTurtle
    currentTurtle['pen'] = True

def show():
    _updateDrawing()

def speed(spd):
    global currentCanvas
    if spd > 0:
        currentCanvas['delay'] = max(round(1000.0 / spd), 1)
    else:
        currentCanvas['delay'] = 0

def bgcolor(colorname):
    global currentCanvas
    currentCanvas['bgcolor'] = colorname

def color(colorname):
    global currentTurtle
    currentTurtle['color'] = colorname

def fillcolor(colorname):
    global currentTurtle
    currentTurtle['fillcolor'] = colorname

def begin_fill():
    global currentTurtle
    currentTurtle['fill'] = True

def end_fill():
    global currentTurtle
    currentTurtle['fill'] = False
    _updateTurtleXY(currentTurtle['x'], currentTurtle['y'], currentTurtle['h'])

def width(w):
    global currentTurtle
    currentTurtle['width'] = w

def showturtle():
    global currentCanvas
    currentCanvas['turtle'] = True

def hideturtle():
    global currentCanvas
    currentCanvas['turtle'] = False

# Color functions - inputs are from 0.0 to 1.0

def color_rgb(r, g, b):
    rgb = [round(i * 255) for i in [r, g, b]]
    return '#' + ''.join(f'{i:02x}' for i in rgb)

def color_hsv(h, s, v):
    rgb = [round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v)]
    return '#' + ''.join(f'{i:02x}' for i in rgb)

def color_random():
    return "#%06x" % random.randint(0, 0xFFFFFF)
