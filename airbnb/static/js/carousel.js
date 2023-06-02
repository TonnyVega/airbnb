document.addEventListener('DOMContentLoaded', function() {
  // Use JavaScript to toggle the show-second-image class on the image-container
  const imageContainer = document.querySelector('.image-container');
  if (imageContainer) {
    imageContainer.addEventListener('click', function() {
      imageContainer.classList.toggle('show-second-image');
    });
  }

  // Slider functionality
  const slides = document.querySelectorAll('.slide');
  if (slides.length > 0) {
    slides.forEach((slide, indx) => {
      slide.style.transform = `translateX(${indx * 100}%)`;
    });

    const nextSlide = document.querySelector('.next-next');
    const prevSlide = document.querySelector('.prev-prev');

    let curSlide = 0;
    let maxSlide = slides.length - 1;

    if (nextSlide) {
      nextSlide.addEventListener('click', function() {
        if (curSlide === maxSlide) {
          curSlide = 0;
        } else {
          curSlide++;
        }

        slides.forEach((slide, indx) => {
          slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
        });
      });
    }

    if (prevSlide) {
      prevSlide.addEventListener('click', function() {
        if (curSlide === 0) {
          curSlide = maxSlide;
        } else {
          curSlide--;
        }

        slides.forEach((slide, indx) => {
          slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
        });
      });
    }
  }
});
