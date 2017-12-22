(function(){
  function getRandomColor() {
    var colors = [
      '29D5FF', 'FFD029', '29FFCD',
      'FA29FF', 'FF2974', 'FFE529'
    ]

    return '#' + colors[Math.floor(Math.random() * 5)];
  }

  $("#categoryContainer").css("background-color", getRandomColor());

  var query = window.location.search.substring(1);
  if (query == 'noautho') {
    setTimeout(function(){showToast()}, 0);
  }

  return(false);
})();

function sayHello() {
  console.log("Hello")
};

function showToast() {
  var x = document.getElementById("snackbar")
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 4000);
};
