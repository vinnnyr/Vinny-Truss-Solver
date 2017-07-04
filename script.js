var myCanvas = document.getElementById("myCanvas");
var formArea=document.getElementById("formArea");
myCanvas.addEventListener("click", clickFunction);

var ctx = myCanvas.getContext("2d");
ctx.fillStyle = "#000000";

var numbNodes= 0;
var nodeCoord=[];
var numbMembs= 0;
var membNodes=[];
var numbReacts=0;
var numbExt=0;
var M=[];
var E=[];

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
}

function zeros(dimensions) {
    var array = [];

    for (var i = 0; i < dimensions[0]; ++i) {
        array.push(dimensions.length == 1 ? 0 : zeros(dimensions.slice(1)));
    }

    return array;
}


function clickFunction(){//This function is called when mouse is clicked in canvas
  pos=getMousePos(myCanvas,event)
  //Circle
  ctx.beginPath();
  ctx.arc(pos.x,pos.y,20,0,2*Math.PI);
  ctx.fill();
}

function nodeQty(){
  numbNodes=document.getElementById("numb");
  numbNodes=numbNodes.value //This is the number of nodes

  M=zeros([2*numbNodes,2*numbNodes])  //Populating the M matrix
  E=zeros([2*numbNodes,1])
  //console.log(M)

  var text="Please enter the x and y coordinates of each node <br><br>"
    for(i=1; i<=numbNodes; i++){
      node="Node " + i
      text+=node
      text+= "<input type='number' id='" + node +"x'>"
      text+= "<input type='number' id='" + node +"y'>"
      text+="<br>"
    }
    text+="<button onclick='nodeCoordinates()'>Submit</button>"
    formArea.innerHTML=text
  }

function nodeCoordinates(){// called at the end of nodeQty
  var nodeArea=document.getElementById("nodes");
  pText="<h2>Nodes</h2><table style='width=100%'><tr><th>Node</th><th>Coordinates</th></tr>"
  for(i=1;i<=numbNodes;i++){
    node="Node " + i
    xCoord=document.getElementById(node+"x").value
    yCoord=document.getElementById(node+"y").value
    nodeCoord[i-1]=[xCoord,yCoord]
    pText+="<tr>" //pText updates the table in the "main" id
    pText+="<th>"+node+"</th>"
    pText+="<th>"+"("+xCoord+","+yCoord+")</th>"
    pText+="</tr>"
    }
    text="How many members? <input type='number' id='numb'><br><button onclick='elementQty()''>Submit</button>"
    formArea.innerHTML=text
    pText+="</table>"
    nodeArea.innerHTML=pText//updates main area with table of node Coordinates
}

function elementQty(){
  numbMembs=document.getElementById("numb");
  numbMembs=numbMembs.value //This is the number of members
  //TO DO: check if numbMembs is viable with numbNodes
  var text=""
    for(i=1; i<=numbMembs; i++){
      memb="Member " + i
      text+=memb
      text+= "<input type='number' id='" + memb +"to'>"
      text+= "<input type='number' id='" + memb +"from'>"
      text+="<br>"
    }
    text+="<button onclick='memberPopulate()'>Submit</button>"
    formArea.innerHTML=text
}

function memberPopulate(){
  var membArea=document.getElementById("membs");
  pText="<h2>Members</h2><table style='width=100%'><tr><th>Member</th><th>Node To</th><th>Node From</th></tr>"
  for(i=1; i<=numbMembs; i++){
    memb="Member " + i
    nodeTo=document.getElementById(memb+"to").value
    nodeFrom=document.getElementById(memb+"from").value
    membNodes[i-1]=[nodeTo,nodeFrom]
    dx=nodeCoord[nodeTo-1][0]-nodeCoord[nodeFrom-1][0]
    dy=nodeCoord[nodeTo-1][1]-nodeCoord[nodeFrom-1][1]
    length=Math.sqrt(dx*dx + dy*dy)
    //Now we must populate M with dx,dy, and length values
    //console.log(length)
    M[2*nodeFrom-2][i-1]=dx/length
    M[2*nodeTo-2][i-1]=-dx/length
    M[2*nodeFrom-1][i-1]=dy/length
    M[2*nodeTo-1][i-1]=-dy/length
    //console.log(M)
    //not sure if that's right.. check for error as we go further^

    pText+="<tr>"
    pText+="<th>"+memb+"</th>"
    pText+="<th>"+nodeTo+"</th>"+"<th>"+nodeFrom+"</th>"
    pText+="</tr>"
  }
  pText+="</table>"
  text="How many reactions? <input type='number' id='numb'><br><button onclick='reactionQty()''>Submit</button>"
  membArea.innerHTML=pText;
  formArea.innerHTML=text;
}
function reactionQty(){
  numbReacts=document.getElementById("numb");
  numbReacts=numbReacts.value //This is the number of reactions
  //TO DO: check if numbMembs is viable with numbNodes
  var text=""
    for(i=1; i<=numbReacts; i++){
      react="Reaction" + i
      text+=react
      text+= "<select id='" + react + "d' name='"+ react+"d'>"
      text+="<option value='x'> Roller X </option>"
      text+="<option value='y'> Roller Y </option>"
      text+="<option value='x and y'> Pin </option>"
      text+="</select>"
      text+="<input type='number' id='"+ react + "node'>"
      text+="<br>"
    }
    text+="<button onclick='assignReactions()'>Submit</button>"
    formArea.innerHTML=text;
}
function assignReactions(){
  //console.log(M)
  for(i=1; i<=numbReacts; i++){
    react="Reaction" + i
    direction=document.getElementById(react+"d")
    direction=direction.value
    node=document.getElementById(react+"node")
    node=node.value
  //   if ((direction == 'y') | (direction == 'Y'))
  //       M(2*node, numberElements+reaction)=M(2*node,numberElements+reaction)+1;
  //  elseif  ((direction=='X') | (direction=='x'))
  //      M(2*node-1, numberElements+reaction)=M(2*node-1,numberElements+reaction)+1;
  //console.log("number of memb" + numbMembs)
  //console.log("this is i" + i)
  numbMembs=Number(numbMembs) //Very important step... I learned this the hard way
    if(direction=='x'){
      M[2*node-2][numbMembs+i-1]=1
    }
    else if (direction=='y') {
      M[2*node-1][numbMembs+i-1]=1
    }
    else if (direction=='x and y') {
      M[2*node-2][numbMembs+i-1]=1
      M[2*node-1][numbMembs+i-1]=1
    }
  }
  text="Enter the number of external forces <input type='number' id='numb'><br><button onclick='extQty()''>Submit</button>"
  formArea.innerHTML=text;
}
function extQty(){
  text=""
  //console.log("Entered here")
  numbExt=document.getElementById('numb').value
  formArea.innerHTML=""
  for(i=1; i<=numbExt; i++){
    extForce="Force "+i;
    text+=extForce + " Node, Value, and Angle"
    text+= "<input type='number' id='" + extForce +"node'>"
    text+= "<input type='number' id='" + extForce +"value'>"
    text+= "<input type='number' id='" + extForce +"angle'>"
    text+="<br>"
  }
  text+="<button onclick='assignExtForces()'>Submit</button>"
  formArea.innerHTML=text
}
function assignExtForces(){
  for(i=1; i<=numbExt; i++){
    extForce="Force "+i;
    node=Number(document.getElementById(extForce +"node").value)
    //console.log(node)
    value=Number(document.getElementById(extForce +"value").value)
    //console.log(value)
    angle=Number(document.getElementById(extForce +"angle").value)
    //console.log(angle)

    //console.log(Math.sin(angle*3.14/180))
    //console.log(-(value*Math.cos(angle*3.14/180)))
    E[node-1]=-(value*Math.sin(angle*3.14/180))
    E[node-2]=-(value*Math.cos(angle*3.14/180))
  }
  console.log(E)
}




//PAST THIS LINE IS a Linear solve library from https://github.com/lovasoa/linear-solve.git
/**
 * Gauss-Jordan elimination
 */

var linear = (function(){
/**
 * Used internally to solve systems
 * If you want to solve A.x = B,
 * choose data=A and mirror=B.
 * mirror can be either an array representing a vector
 * or an array of arrays representing a matrix.
 */
function Mat(data, mirror) {
  // Clone the original matrix
  this.data = new Array(data.length);
  for (var i=0, cols=data[0].length; i<data.length; i++) {
    this.data[i] = new Array(cols);
    for(var j=0; j<cols; j++) {
      this.data[i][j] = data[i][j];
    }
  }

  if (mirror) {
    if (typeof mirror[0] !== "object") {
      for (var i=0; i<mirror.length; i++) {
        mirror[i] = [mirror[i]];
      }
    }
    this.mirror = new Mat(mirror);
  }
}

/**
 * Swap lines i and j in the matrix
 */
Mat.prototype.swap = function (i, j) {
  if (this.mirror) this.mirror.swap(i,j);
  var tmp = this.data[i];
  this.data[i] = this.data[j];
  this.data[j] = tmp;
}

/**
 * Multiply line number i by l
 */
Mat.prototype.multline = function (i, l) {
  if (this.mirror) this.mirror.multline(i,l);
  var line = this.data[i];
  for (var k=line.length-1; k>=0; k--) {
    line[k] *= l;
  }
}

/**
 * Add line number j multiplied by l to line number i
 */
Mat.prototype.addmul = function (i, j, l) {
  if (this.mirror) this.mirror.addmul(i,j,l);
  var lineI = this.data[i], lineJ = this.data[j];
  for (var k=lineI.length-1; k>=0; k--) {
    lineI[k] = lineI[k] + l*lineJ[k];
  }
}

/**
 * Tests if line number i is composed only of zeroes
 */
Mat.prototype.hasNullLine = function (i) {
  for (var j=0; j<this.data[i].length; j++) {
    if (this.data[i][j] !== 0) {
      return false;
    }
  }
  return true;
}

Mat.prototype.gauss = function() {
  var pivot = 0,
      lines = this.data.length,
      columns = this.data[0].length,
      nullLines = [];

  for (var j=0; j<columns; j++) {
    // Find the line on which there is the maximum value of column j
    var maxValue = 0, maxLine = 0;
    for (var k=pivot; k<lines; k++) {
      var val = this.data[k][j];
      if (Math.abs(val) > Math.abs(maxValue)) {
        maxLine = k;
        maxValue = val;
      }
    }
    if (maxValue === 0) {
      // The matrix is not invertible. The system may still have solutions.
      nullLines.push(pivot);
    } else {
      // The value of the pivot is maxValue
      this.multline(maxLine, 1/maxValue);
      this.swap(maxLine, pivot);
      for (var i=0; i<lines; i++) {
        if (i !== pivot) {
          this.addmul(i, pivot, -this.data[i][j]);
        }
      }
    }
    pivot++;
  }

  // Check that the system has null lines where it should
  for (var i=0; i<nullLines.length; i++) {
    if (!this.mirror.hasNullLine(nullLines[i])) {
      throw new Error("singular matrix");
    }
  }
  return this.mirror.data;
}

/**
 * Solves A.x = b
 * @param A
 * @param b
 * @return x
 */
exports.solve = function solve(A, b) {
  var result = new Mat(A,b).gauss();
  if (result.length > 0 && result[0].length === 1) {
    // Convert Nx1 matrices to simple javascript arrays
    for (var i=0; i<result.length; i++) result[i] = result[i][0];
  }
  return result;
}

function identity(n) {
  var id = new Array(n);
  for (var i=0; i<n; i++) {
    id[i] = new Array(n);
    for (var j=0; j<n; j++) {
      id[i][j] = (i === j) ? 1 : 0;
    }
  }
  return id;
}

/**
 * invert a matrix
 */
exports.invert = function invert(A) {
  return new Mat(A, identity(A.length)).gauss();
}

return exports;
})();

if (typeof module.exports === "object") module.exports = linear;
