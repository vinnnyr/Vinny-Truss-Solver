// var numbNodes = 0;
// var nodeCoord = [];
// var numbMembs = 0;
// var membNodes = [];
// var numbReacts = 0;
// var numbExt = 0;
// var M = [];
// var E = [];
var formArea = document.getElementById("formArea");

function createButton() {
  formArea.innerHTML = '<form id="myForm"><textarea form="myForm" id="fileIn"  value="Paste truss here" rows="10" cols="50"></textarea> <br> <button type="button" id="fileSubmit" class="btn btn-default" onclick="fileReader()">Submit</button></form>'
}

function splitText(string, char) {
  a = string.substring(0, string.indexOf(char))
  b = string.substring(string.indexOf(char) + 1, string.length - 1)
  return [a, b];
}

function splitText2(string, char) {
  a = string.substring(0, string.indexOf(char))
  b = string.substring(string.indexOf(char) + 1, string.length)
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
  //console.log(numbNodes)
  //console.log(restText)

  //Reading Node Data
  for (i = 1; i <= numbNodes; i++) {
    node = Number(splitText(restText, " ")[0])
    restText = splitText(restText, " ")[1]
    //console.log(node)
    //console.log(restText)
    xCoord = Number(splitText(restText, " ")[0])
    restText = splitText(restText, " ")[1]
    //console.log(xCoord)
    yCoord = Number(splitText(restText, "\n")[0])
    restText = splitText(restText, "\n")[1]
    //console.log(yCoord)
    //restText = splitText(restText,"\n")[1]
    nodeCoord[i - 1] = [xCoord, yCoord]
    //console.log(nodeCoord)
  }
  //console.log(nodeCoord)
  populateZeros();

  //To Do: Make sure all variables scraped from text are numbers, and not blank
  membTextToRead = textToRead.substring(textToRead.indexOf("M") + 1, textToRead.indexOf("R") - 1)
  numbMembs = splitText(membTextToRead, "\n")[0]
  restText = splitText(restText, "\n")[1]
  //console.log(numbMembs)
  //Reading Member Data
  for (i = 1; i <= numbMembs; i++) {
    member = Number(splitText(restText, " ")[0])
    restText = splitText(restText, " ")[1]
    //console.log("Member" + String(member))
    nodeTo = Number(splitText(restText, " ")[0])
    restText = splitText(restText, " ")[1]
    //console.log(nodeTo)
    nodeFrom = Number(splitText(restText, "\n")[0])
    restText = splitText(restText, "\n")[1]
    //console.log(nodeFrom)
    membNodes[i - 1] = [nodeTo, nodeFrom]
    dx = nodeCoord[nodeTo - 1][0] - nodeCoord[nodeFrom - 1][0]
    dy = nodeCoord[nodeTo - 1][1] - nodeCoord[nodeFrom - 1][1]
    length = Math.sqrt(dx * dx + dy * dy)
    //console.log([dx, dy, length])
    //Now we must populate M with dx,dy, and length values
    //console.log(length)
    M[2 * nodeFrom - 2][i - 1] = dx / length
    M[2 * nodeTo - 2][i - 1] = -dx / length
    M[2 * nodeFrom - 1][i - 1] = dy / length
    M[2 * nodeTo - 1][i - 1] = -dy / length
    //console.log(M)
  }
  //Reading Reaction Data
  reactionTextToRead = textToRead.substring(textToRead.indexOf("R") + 1, textToRead.indexOf("E"))
  numbReacts = reactionTextToRead[0];
  restText = reactionTextToRead.substring(reactionTextToRead.indexOf("\n") + 1, reactionTextToRead.length) //idk why it isnts -1
  //console.log(numbReacts)
  //To Do: Ensure that numbReacts+numbMembs==numbNodes*2
  for (i = 1; i <= numbReacts; i++) {
    reaction = splitText2(restText, " ")[0]
    restText = splitText2(restText, " ")[1]
    //console.log(reaction)
    node = splitText2(restText, " ")[0]
    restText = splitText2(restText, " ")[1]
    ///console.log(node)
    direction = splitText2(restText, "\n")[0]
    restText = splitText2(restText, "\n")[1]
    numbMembs = Number(numbMembs) //Very important step... I learned this the hard way
    ///console.log(direction)

    reacts[i - 1] = []
    reacts[i - 1][0] = i
    reacts[i - 1][1] = node
    reacts[i - 1][2] = direction

    if (direction == 'x' || direction == 'X') {
      M[2 * node - 2][numbMembs + i - 1] = M[2 * node - 2][numbMembs + i - 1] + 1
    } else if (direction == 'y' || direction == 'Y') {
      M[2 * node - 1][numbMembs + i - 1] = M[2 * node - 2][numbMembs + i - 1] + 1
    }
  }

  //Reading External Force Data
  externalTextToRead = splitText2(textToRead, ("E"))[1]
  //console.log(externalTextToRead)
  numbExt = splitText2(externalTextToRead, "\n")[0]
  restText = splitText2(externalTextToRead, "\n")[1]
  for (i = 1; i <= numbExt; i++) {
    node = splitText2(restText, " ")[0]
    restText = splitText2(restText, " ")[1]
    //console.log(node)
    value = splitText2(restText, " ")[0]
    restText = splitText2(restText, " ")[1]
    //console.log(value)
    angle = splitText2(restText, "\n")[0]
    restText = splitText2(restText, "\n")[1]
    //console.log(angle)
    externals[i - 1] = [];
    externals[i - 1][0] = node;
    externals[i - 1][1] = value;
    externals[i - 1][2] = angle;

    E[2 * node - 1] = -(value * Math.sin(angle * Math.PI / 180))
    E[2 * node - 2] = -(value * Math.cos(angle * Math.PI / 180))
  }
  numbMembs = Number(numbMembs);
  numbReacts = Number(numbReacts);
  numbNodes = Number(numbNodes);
  if (2 * numbNodes == numbMembs + numbReacts) {
    solveAndDisplay();
    canvasDrawer();
  } else {
    formArea.innerHTML = "<h3>Some error happened. Please make sure the input is correct, or try again by refreshing the page </h3>"
  }
  //end of Function fileReader()
}
