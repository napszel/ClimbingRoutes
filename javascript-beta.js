$(document).ready(function() {
  var startHash = window.location.search; // the text after the ? in the path
  if (startHash) {
    $(".opinion").click(function() {
      if ($(this).hasClass("faded")) {
	$(this).removeClass("faded");
	if (this.id == 'hard') {
	  $("#easy").addClass("faded");
	} else {
	  if (this.id == 'easy') {
	    $("#hard").addClass("faded");
	  }
	}
      } else {
	$(this).addClass("faded");
      }
    });

    $(".result-button").click(function() {
      if ($(this).hasClass("clicked-result-button")) {
	$(".result-button").removeClass("clicked-result-button");
	$("#results-form").find("input[type=radio]").prop('checked', false);
      } else {
	$(".result-button").removeClass("clicked-result-button");
	$("#results-form").find("input[type=radio]").prop('checked', false);
	$(this).addClass("clicked-result-button");
	if (this.id == 'attempt-button') {
	  $("#attempt1").prop('checked', true);
	}
      }
    });

    $(".radio").click(function() {
      $(".result-button").removeClass("clicked-result-button");
      $("#attempt-button").addClass("clicked-result-button");
    });
  }
} );

