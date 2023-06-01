$(document).ready(function() {
  $(".dropdown-toggle").click(function() {
    $(this).toggleClass("active");
    $(".dropdown-menu").slideToggle();
  });
});


// Add JavaScript code to handle the dismiss button functionality
document.addEventListener('DOMContentLoaded', function() {
  var closeButtons = document.getElementsByClassName('close');
  for (var i = 0; i < closeButtons.length; i++) {
    closeButtons[i].addEventListener('click', function() {
      this.parentElement.parentElement.parentElement.removeChild(this.parentElement.parentElement);
    });
  }

  var flashMessages = document.getElementsByClassName('flash-message');
  for (var i = 0; i < flashMessages.length; i++) {
    flashMessages[i].classList.add('show');
  }
});

function wish(){
  alert('added to wishlist')
}


// footer
var footer = document.getElementById("footer");
var prevScrollPos = window.scrollY || window.pageYOffset;

window.onscroll = function() {
  var currentScrollPos = window.scrollY || window.pageYOffset;
  if (prevScrollPos > currentScrollPos) {
    footer.style.display = "block";
  } else {
    footer.style.display = "none";
  }
  prevScrollPos = currentScrollPos;
};


// add apartment 
const openModalButton = document.querySelector('.open-modal');
const modal = document.querySelector('#myModal');
const closeModalButton = modal.querySelector('.close');

openModalButton.addEventListener('click', function() {
  modal.style.display = 'block';
});

closeModalButton.addEventListener('click', function() {
  modal.style.display = 'none';
});

window.addEventListener('click', function(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});