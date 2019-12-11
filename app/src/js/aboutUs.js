let bbdy = document.querySelector("body");
let h = $("section").css("height");
let img0 = document.getElementById("img0");
let img00 = document.getElementById("img00");
let title = document.getElementById("title");
let allSection = document.querySelectorAll("section");
let item = document.getElementsByClassName("third-block__content__elements");
let h11 = document.querySelector("h1");

$(document).scroll(function() {
  let userPosition = Math.round(
    (window.innerHeight + pageYOffset) / document.documentElement.clientHeight
  );

  let userPositionAbsolute =
    (window.innerHeight + pageYOffset) / document.documentElement.clientHeight;

  for (var i = 0; i < allSection.length; i++) {
    allSection[i].style.backgroundImage = "url(/src/img/aboutUs/anim.gif)";
  }

  console.log(userPosition);
  if (userPosition > 0) {
    bbdy.style.background = "#1A1A1A";
    // document.querySelector("h1").classList.add("h1new");
  }

  for (var i = 0; i < item.length; i++) {
    if (userPositionAbsolute > 2.6 && userPositionAbsolute < 3.6) {
      item[0].classList.add("fix");
    }

    if (userPositionAbsolute > 4 && userPositionAbsolute < 4.8) {
      item[0].classList.remove("fix");
      item[1].classList.add("fix");
    }

    if (userPositionAbsolute > 5.6 && userPositionAbsolute < 6.5) {
      item[1].classList.remove("fix");
      item[2].classList.add("fix");
    }

    if (userPositionAbsolute > 6.9 && userPositionAbsolute < 7.8) {
      item[2].classList.remove("fix");
      item[3].classList.add("fix");
    }

    if (userPositionAbsolute > 8.2 && userPositionAbsolute < 9.19) {
      item[3].classList.remove("fix");
      item[4].classList.add("fix");
    } else {
      item[i].classList.remove("fix");
    }
  }

  if (userPositionAbsolute > 1.5 && userPositionAbsolute < 2) {
    img0.style.opacity = userPositionAbsolute - 1;
    title.style.opacity = userPositionAbsolute - 1;
    img00.style.opacity = userPositionAbsolute - 1;
  } else {
    img0.style.opacity = 0;
    title.style.opacity = 0;
    img00.style.opacity = 0;
  }

  console.log(userPositionAbsolute);
});

let revert0 = function() {
  bbdy.style.background = "#9c27b0";
  for (var i = 0; i < allSection.length; i++) {
    allSection[i].style.backgroundImage = "none";
  }
};

let revert = function() {
  setTimeout(revert0, 2500);
};
