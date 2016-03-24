$(document).ready(function() {
  $("header").hide()
  $("header").fadeIn(1500);
  $(".content").hide()
  setTimeout(function() {
    $(".content").fadeIn(1500);
  }, 300);

  $("#menu-icon").click(function() {
    $(".menu").toggle();

    $(".content").toggle(function() {
      $(this).toggleClass('menu-out menu-up');
    }, function() {
      $(this).toggleClass('menu-up menu-out');
    });
  });

  // $("#brief-it").click(function() {
  //   $("#spin-load").toggle();
  //
  //   // $(".content").toggle(function() {
  //   //   $(this).toggleClass('menu-out menu-up');
  //   // }, function() {
  //   //   $(this).toggleClass('menu-up menu-out');
  //   // });
  // });

  // $(".menu li a").click(function() {
  //   $(".menu").toggle();
  //   $(".menu").toggle();
  // });

  // });

  switch (window.location.pathname) {
    case "/":
      $("#homelink").removeClass("notcurrent").addClass("nobottom");
      break;
    case "/about":
      $("#aboutlink").removeClass("notcurrent").addClass("nobottom");
      break;
    case "/ussc":
      $("#ussclink").removeClass("notcurrent").addClass("nobottom");
      break;
  }
});
