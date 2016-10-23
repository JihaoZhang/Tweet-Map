var btn = document.getElementById("submit");
btn.addEventListener("click", function(){
    var q = document.getElementById("search");
    window.location = "/?q=" + q.value;
});
