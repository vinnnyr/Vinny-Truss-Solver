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
