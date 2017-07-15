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

  // console.log(maxs)
  // console.log(mins)
  // console.log(sizes)
  // console.log(deltas)
  // console.log(scale)


  //Drawing of the nodes
  for(i=1;i<=numbNodes;i++){
    x=nodeCoord[i-1][0]*scale/2 + width/10;
    y=height-nodeCoord[i-1][1]*scale/2 - height/10;
    scaledNodeCoord[i-1]=[x,y];
    ctx.beginPath();
    ctx.arc(x,y,10,0,2*Math.PI);
    ctx.stroke();
    ctx.fill();
    ctx.font = "12px Arial";
    ctx.fillText("Node" + String(i),x+width/40,y);
  }
  //Drawing of the members
  for(i=0;i<numbMembs;i++){
    nodes=membNodes[i];
    nA=nodes[0];
    nB=nodes[1];
    //aCoord=[nodeCoord[nA-1][0]*scale/2 + width/10,height-nodeCoord[nA-1][1]*scale/2-height/10]
    //bCoord=[nodeCoord[nB-1][0]*scale/2 + width/10,height-nodeCoord[nB-1][1]*scale/2-height/10]
    aCoord=scaledNodeCoord[nA-1];
    bCoord=scaledNodeCoord[nB-1];
    ctx.beginPath();
    ctx.moveTo(aCoord[0],aCoord[1])
    ctx.lineTo(bCoord[0],bCoord[1])
    ctx.stroke();
  }
  //drawImage('arrow.png',[100,200],90)
  //drawImage('https://mdn.mozillademos.org/files/5397/rhino.jpg',aCoord)

  //Drawing of the reactions
  for(i=1;i<=numbReacts;i++){
    mat=reacts[i-1];
    //console.log(reacts[i-1])
    //console.log(mat);
    pos=scaledNodeCoord[mat[1]-1]
    console.log(pos)
    direction=mat[2]
    if (direction == 'x' || direction=='X') {
      drawImage('arrow.png',pos,90)
    }
    else if(direction=='y' || direction=='Y'){
      drawImage('arrow.png',pos,0)
    }
  }

  for(i=1;i<=externals.length;i++){
    ee=externals[i-1];
    pos=scaledNodeCoord[ee[0]-1];
    drawImage('arrow.png',pos,Number(ee[2])+90)
  }
}

function drawImage(imgPath,pos,theta){
  var imageObj = new Image();
      imageObj.onload = function() {
        ctx.save();
        //console.log(theta*Math.PI/180)
        ctx.translate(pos[0]-5,pos[1]+5)
        ctx.rotate(theta*Math.PI/180)
        ctx.translate(-pos[0]+5,-pos[1]-5)
        ctx.drawImage(imageObj, pos[0]-5,pos[1]+5,10,15);
        ctx.restore();
      }
      imageObj.src = imgPath;
}
