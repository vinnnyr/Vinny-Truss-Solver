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
    console.log(node)
    value=Number(document.getElementById(extForce +"value").value)
    //console.log(value)
    angle=Number(document.getElementById(extForce +"angle").value)
    //console.log(angle)

    //console.log(Math.sin(angle*3.14/180))
    //console.log(-(value*Math.cos(angle*3.14/180)))
    E[node]=-(value*Math.sin(angle*Math.PI/180))
    E[node-1]=-(value*Math.cos(angle*Math.PI/180))
  }
  console.log(E)
  var Mi=numeric.inv(M)
  console.log(numeric.dot(Mi,E))
}
