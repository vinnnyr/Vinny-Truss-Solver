var myCanvas = document.getElementById("myCanvas");
var formArea = document.getElementById("formArea");

// document.addEventListener('DOMContentLoaded', function() {
//   onLoad();
// }, false);

var numbNodes = 0;
var nodeCoord = [];
var numbMembs = 0;
var membNodes = [];
var numbReacts = 0;
var numbExt = 0;
var M = [];
var E = [];

function zeros(dimensions) {
  var array = [];
  for (var i = 0; i < dimensions[0]; ++i) {
    array.push(dimensions.length == 1 ? 0 : zeros(dimensions.slice(1)));
  }
  return array;
}


function onLoad() {
  formArea.innerHTML = 'How many nodes? <input type="number" id="numb"><br><button type="submit" onclick="nodeQty()">Submit</button>'
}

function nodeQty() {
  numbNodes = document.getElementById("numb");
  numbNodes = numbNodes.value //This is the number of nodes
  populateZeros();

  //console.log(M)

  var text = "Please enter the x and y coordinates of each node <br><br>"
  for (i = 1; i <= numbNodes; i++) {
    node = "Node " + i
    text += node
    text += "<input type='number' id='" + node + "x'>"
    text += "<input type='number' id='" + node + "y'>"
    text += "<br>"
  }
  text += "<button onclick='nodeCoordinates()' type='submit' >Submit</button>"
  formArea.innerHTML = text
}

function populateZeros(){
  M = zeros([2 * numbNodes, 2 * numbNodes]) //Populating the M matrix
  E = zeros([2 * numbNodes, 1])
}

function nodeCoordinates() { // called at the end of nodeQty
  var nodeArea = document.getElementById("nodes");
  pText = "<h2>Nodes</h2><table style='width=100%'><tr><th>Node</th><th>Coordinates</th></tr>"
  for (i = 1; i <= numbNodes; i++) {
    node = "Node " + i
    xCoord = document.getElementById(node + "x").value
    yCoord = document.getElementById(node + "y").value
    nodeCoord[i - 1] = [xCoord, yCoord]
    pText += "<tr>" //pText updates the table in the "main" id
    pText += "<th>" + node + "</th>"
    pText += "<th>" + "(" + xCoord + "," + yCoord + ")</th>"
    pText += "</tr>"
  }
  text = "How many members? <input type='number' id='numb'><br><button onclick='elementQty()' type='submit' '>Submit</button>"
  formArea.innerHTML = text
  pText += "</table>"
  nodeArea.innerHTML = pText //updates main area with table of node Coordinates
}

function elementQty() {
  numbMembs = document.getElementById("numb");
  numbMembs = numbMembs.value //This is the number of members
  //TO DO: check if numbMembs is viable with numbNodes
  var text = ""
  for (i = 1; i <= numbMembs; i++) {
    memb = "Member " + i
    text += memb
    text += "<input type='number' id='" + memb + "to'>"
    text += "<input type='number' id='" + memb + "from'>"
    text += "<br>"
  }
  text += "<button onclick='memberPopulate() ' type='submit'>Submit</button>"
  if (numbMembs >= numbNodes) { //numb membs CANNOT be less than numb Nodes
    formArea.innerHTML = text
  } else {
    formArea.innerHTML = "<h3>Number of members cannnot be less than number of nodes, please refresh to try again </h3>"
  }
}

function memberPopulate() {
  var membArea = document.getElementById("membs");
  pText = "<h2>Members</h2><table style='width=100%'><tr><th>Member</th><th>Node To</th><th>Node From</th></tr>"
  for (i = 1; i <= numbMembs; i++) {
    memb = "Member " + i
    nodeTo = document.getElementById(memb + "to").value
    nodeFrom = document.getElementById(memb + "from").value
    membNodes[i - 1] = [nodeTo, nodeFrom]
    dx = nodeCoord[nodeTo - 1][0] - nodeCoord[nodeFrom - 1][0]
    dy = nodeCoord[nodeTo - 1][1] - nodeCoord[nodeFrom - 1][1]
    length = Math.sqrt(dx * dx + dy * dy)
    //Now we must populate M with dx,dy, and length values
    //console.log(length)
    M[2 * nodeFrom - 2][i - 1] = dx / length
    M[2 * nodeTo - 2][i - 1] = -dx / length
    M[2 * nodeFrom - 1][i - 1] = dy / length
    M[2 * nodeTo - 1][i - 1] = -dy / length
    //console.log(M)
    //not sure if that's right.. check for error as we go further^

    pText += "<tr>"
    pText += "<th>" + memb + "</th>"
    pText += "<th>" + nodeTo + "</th>" + "<th>" + nodeFrom + "</th>"
    pText += "</tr>"
  }
  pText += "</table>"
  text = "How many reactions? <input type='number' id='numb'><br><button onclick='reactionQty()'' type='submit'>Submit</button>"
  membArea.innerHTML = pText;
  formArea.innerHTML = text;
}

function reactionQty() {
  numbReacts = document.getElementById("numb");
  numbReacts = numbReacts.value //This is the number of reactions
  //TO DO: check if numbMembs is viable with numbNodes
  var text = ""
  for (i = 1; i <= numbReacts; i++) {
    react = "Reaction" + i
    text += react
    text += "<select id='" + react + "d' name='" + react + "d'>"
    text += "<option value='x'> X </option>"
    text += "<option value='y'> Y </option>"
    text += "</select>"
    text += "<input type='number' id='" + react + "node'>"
    text += "<br>"
  }
  text += "<button onclick='assignReactions()'>Submit</button>"
  if (numbNodes * 2 == numbReacts + numbMembs) {
    formArea.innerHTML = text;
  } else {
    formArea.innerHTML = "<h3>Error:Statically indeterminate. Please try again by refreshing the page </h3>"
  }
}

function assignReactions() {
  //console.log(M)
  for (i = 1; i <= numbReacts; i++) {
    react = "Reaction" + i
    direction = document.getElementById(react + "d")
    direction = direction.value
    node = document.getElementById(react + "node")
    node = node.value
    numbMembs = Number(numbMembs) //Very important step... I learned this the hard way
    if (direction == 'x') {
      M[2 * node - 2][numbMembs + i - 1] = M[2 * node - 2][numbMembs + i - 1] + 1
    } else if (direction == 'y') {
      M[2 * node - 1][numbMembs + i - 1] = M[2 * node - 2][numbMembs + i - 1] + 1
    }
  }
  text = "Enter the number of external forces <input type='number' id='numb'><br><button onclick='extQty()''>Submit</button>"
  formArea.innerHTML = text;
}

function extQty() {
  text = ""
  //console.log("Entered here")
  numbExt = document.getElementById('numb').value
  formArea.innerHTML = ""
  for (i = 1; i <= numbExt; i++) {
    extForce = "Force " + i;
    text += extForce + " Node, Value, and Angle"
    text += "<input type='number' id='" + extForce + "node'>"
    text += "<input type='number' id='" + extForce + "value'>"
    text += "<input type='number' id='" + extForce + "angle'>"
    text += "<br>"
  }
  text += "<button onclick='assignExtForces()' type='submit' >Submit</button>"
  formArea.innerHTML = text
}

function assignExtForces() {
  for (i = 1; i <= numbExt; i++) {
    extForce = "Force " + i;
    node = Number(document.getElementById(extForce + "node").value)
    //console.log(node)
    value = Number(document.getElementById(extForce + "value").value)
    //console.log(value)
    angle = Number(document.getElementById(extForce + "angle").value)
    //console.log(angle)

    //console.log(Math.sin(angle*3.14/180))
    //console.log(-(value*Math.cos(angle*3.14/180)))
    E[2 * node - 1] = -(value * Math.sin(angle * Math.PI / 180))
    E[2 * node - 2] = -(value * Math.cos(angle * Math.PI / 180))
  }
  //console.log(E)
  solveAndDisplay()
}
function solveAndDisplay(){
  var Mi = numeric.inv(M)
  A = numeric.dot(Mi, E)
  //Mtable=document.getElementById('M');
  //Mtable.innerHTML=makeTableHTML(M)

  text = "<h2>Results</h2><table><tr> <th>Type </th><th>Value</th></tr> "
  for (i = 1; i <= 2 * numbNodes; i++) {
    text += "<tr>"
    text += "<td>"
    if (i <= numbMembs) {
      text += "Member " + i
    } else {
      text += "Reaction " + String(Number(i) - Number(numbMembs))
    }
    text += "</td>"
    //console.log(String(A[i-1]))
    text += "<td>" + String(A[i - 1]) + "</td>"
    text += "</tr>"
  }
  text += "</table>"

  Atable = document.getElementById('A');
  formArea.innerHTML = ""
  Atable.innerHTML = text
}

function makeTableHTML(myArray) {
  var result = "<table>";
  for (var i = 0; i < myArray.length; i++) {
    result += "<tr>";
    for (var j = 0; j < myArray[i].length; j++) {
      result += "<td>" + myArray[i][j] + "</td>";
    }
    result += "</tr>";
  }
  result += "</table>";

  return result;
}
