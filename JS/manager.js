f = document.getElementById("Forms");
t = document.getElementById("Txt file");
man=document.getElementById("managerArea")

function choosePath() {
  if (f.checked) {
    onLoad();
  } else if (t.checked) {
    createButton();
  }
  man.innerHTML=""
}
function canvasDrawer(){//only to be called after truss is solved
  //console.log("Entered Canvas Drawer")
  myCanvas.width=window.innerWidth/2;
  myCanvas.height=window.innerHeight/2;
  ctx=myCanvas.getContext("2d");
  //First we must collect data and come up with a scale factor
  var width = myCanvas.scrollWidth;
  var height = myCanvas.scrollHeight;
  var maxs= [twoDMax(nodeCoord,0),twoDMax(nodeCoord,1)];
  var mins = [twoDMin(nodeCoord,0),twoDMin(nodeCoord,1)];
  var sizes = [width,height];

  if(width>=height){//the smaller of the two values will be the target
    target=height;
  }
  else{
    target=width;
  }
  deltas=[maxs[0]-mins[0],maxs[0]-mins[0]]

  if(deltas[0]>=deltas[1]){//pick the smaller of the deltas
    delta=deltas[1]
  }
  else{
    delta=deltas[0]
  }

  scale=target/delta

  console.log(maxs)
  console.log(mins)
  console.log(sizes)
  console.log(deltas)
  console.log(scale)


  //Drawing of the nodes
  for(i=1;i<=numbNodes;i++){
    x=nodeCoord[i-1][0]*scale/2 + width/10;
    y=height-nodeCoord[i-1][1]*scale/2 - height/10;
    ctx.beginPath();
    ctx.arc(x,y,10,0,2*Math.PI);
    ctx.stroke();
    ctx.font = "30px Arial";
    ctx.fillText("Node" + String(i),x,y);
  }
}
