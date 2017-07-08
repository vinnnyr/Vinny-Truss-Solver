// var numbNodes = 0;
// var nodeCoord = [];
// var numbMembs = 0;
// var membNodes = [];
// var numbReacts = 0;
// var numbExt = 0;
// var M = [];
// var E = [];

function createButton() {
  formArea.innerHTML = '<form id="myForm"><textarea form="myForm" id="fileIn"  value="Paste truss here" rows="4" cols="50"></textarea> <br> <input type="button" id="fileSubmit" onclick="fileReader()"></input></form>'
}

function splitText(string, char) {
  a = string.substring(0, string.indexOf(char))
  b = string.substring(string.indexOf(char) + 1, string.length - 1)
  return [a, b];
}

function fileReader() {
  //TO DO: make large text box, ask user to paste values... read that
  //to do on forms.js-- output node geo/external into a text file
  //console.log("File read");
  textToRead = document.getElementById("myForm").fileIn.value;
  //console.log(textToRead);
  //formArea.innerHTML = textToRead;
  numbNodes = Number(splitText(textToRead, "\n")[0][1])
  restText = splitText(textToRead, "\n")[1] // This var will store the rest of the text to read
  console.log(numbNodes)
  //console.log(restText)

  //Reading Node Data
  for (i = 1; i <= numbNodes; i++) {
    node = Number(splitText(restText," ")[0])
    restText = splitText(restText," ")[1]
    console.log(node)
    //console.log(restText)
    xCoord = Number(splitText(restText," ")[0])
    restText = splitText(restText," ")[1]
    console.log(xCoord)
    yCoord = Number(splitText(restText,"\n")[0])
    restText = splitText(restText,"\n")[1]
    console.log(yCoord)
    //restText = splitText(restText,"\n")[1]
    nodeCoord[i - 1] = [xCoord, yCoord]
    console.log(nodeCoord)
  }
  console.log(nodeCoord)
  populateZeros();

  //To Do: Make sure all variables scraped from text are numbers, and not blank

  //numbMembs=Number(splitText(restText, "\n")[0])
  membTextToRead=textToRead.substring(textToRead.indexOf("M")+1,textToRead.indexOf("R")-1)
  numbMembs=splitText(membTextToRead,"\n")[0]
  restText=splitText(restText, "\n")[1]
  console.log(numbMembs)
  for (i=1;i<=numbMembs;i++){
    member = Number(splitText(restText," ")[0])
    restText = splitText(restText," ")[1]
    console.log("Member" + String(member))
    nodeTo= Number(splitText(restText," ")[0])
    restText = splitText(restText," ")[1]
    console.log(nodeTo)
    nodeFrom= Number(splitText(restText,"\n")[0])
    restText = splitText(restText,"\n")[1]
    console.log(nodeFrom)
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
  }

//end of Function fileReader()
}
