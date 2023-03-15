// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("imgReport");
var modalImg = document.getElementById("img01");
// var captionT ext = document.getElementById("caption");
img.onclick = function(){
    modal.style.display = "flex";
    modalImg.src = this.src;
    // captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
    modal.style.display = "none";
}
document.onkeydown = function(evt) {
evt = evt || window.event;
var isEscape = false;
if ("key" in evt) {
    isEscape = (evt.key === "Escape" || evt.key === "Esc");
} else {
    isEscape = (evt.keyCode === 27);
}
if (isEscape) {
    modal.style.display = "none";
}
};