f = document.getElementById("Forms");
t = document.getElementById("Txt file");

function choosePath() {
  if (f.checked) {
    onLoad();
  } else if (t.checked) {
    createButton();
  }
}