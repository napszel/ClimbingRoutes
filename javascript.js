function getColorFromGrade(grade, type) {
  if (type == "Sport") {
    var no = parseInt(grade.substring(0, 1));
    var l = grade.substring(1, 2);
    if (no < 5) return "yellow";
    if (no == 5) {
      if (l == "c") {
	return "blue";
      } else {
	return "yellow";
      }
    }
    if (no == 6) {
      if (l == "c") {
	return "red";
      } else {
	return "blue";
      }
    }
    if (no == 7) {
      if (l == "c") {
	return "black";
      } else {
	return "red";
      }
    }
    if (no > 7) {
      return "black";
    }
  } else {
    var no = parseInt(grade.substring(1, 2));
    if (no <= 1) {
      return "yellow";
    }
    if (no == 2) {
      return "green";
    }
    if (no == 3) {
      return "blue";
    }
    if (no == 4) {
      return "red";
    }
    if (no >= 5) {
      return "black";
    }
  }
}

var special_letters = [
  ['ä', 'a'],
  ['ö', 'o'],
  ['ü', 'u'],
  [',', ' ']
];

function replaceSpecialLetters(text) {
  for (var i=0; i<special_letters.length; i++) {
    text = text.replace(special_letters[i][0], special_letters[i][1]);
  }
  return text;
}

function applyFilter(word, field) {
  if ($(field).val() != word) {
    $(field).val(word);
  } else {
    $(field).val("");
  }
  $(field).trigger('input');
}

$(document).ready(function() {
  var startHash = window.location.search; // the text after the ? in the path
  if (!startHash) {
    $("#main_table").show();

    // Setup - add a text input to each footer cell -> search boxes for each column
    // - also create the array with default searches
    var default_search_values = []
    $('#example tfoot th').each( function () {
      var title = $(this)[0].attributes['title'].value;
      var placeholder = $(this)[0].attributes['placeholder'].value;
      var default_value = ""
      if ($(this)[0].attributes['default']) {
	default_value = $(this)[0].attributes['default'].value;
	default_search_values.push({"sSearch": default_value});
      } else {
	default_search_values.push(null);
      }
      $(this).html( '<input id="'+title+'-filter" type="text" placeholder="'+placeholder+'" value="'+default_value+'"/>' );
    } );
    
    // DataTable
    var table = $('#example').DataTable( {
      "order": [5, 'desc'],
      "pageLength": -1,
      "paging": false,
      "bAutoWidth": false,
      "columnDefs": [
	{ "width": "20px", "targets": [ "twenty" ] },
	{ "width": "40px", "targets": [ "fourty" ] },
	{ "width": "60px", "targets": [ "sixty" ] },
	{ "width": "90px", "targets": [ "ninety" ] },
	{ "width": "110px", "targets": [ "hundredten" ] },
	{ "width": "200px", "targets": [ "twohundred" ] },
	{ "visible": false, "targets": [4, 8, 11, 12] }
      ],
      "dom": 'ifBrt',
      "buttons": [
        'colvis'
      ],
      "aoSearchCols": default_search_values
    } );

    // Apply the search
    table.columns().every( function () {
      var that = this;
      
      $( 'input', this.footer() ).on('input', function () {
	if ( that.search() !== this.value ) {
          that
            .search( this.value, true )
            .draw();
	}
      } );
    } );

    // Apply the filter from path if any
    var startFilter = window.location.hash; // the text after the # in the path
    if (startFilter) {
      applyFilter(decodeURIComponent(startFilter.substring(1)), '#sector-filter');
    }
  } else {
    parts = startHash.split(":");
    date = parts[0].split("=")[1];
    type = parts[1]
    place = parts[2]
    number = parts[3]
    if (place == 'gas') {
      place = "Gaswerk";
    } else {
      place = "Milandia";
    }
    if (type == 'bould') {
      type = "Boulder";
    } else {
      type = "Sport";
    }
    $("#title-div").append("<label class=\"title\"><span class=\"emphasis\">" + type + "</span> route <span class=\"emphasis\">#" + number + "</span> of <span class=\"emphasis\">" + place + "</span> set on <span class=\"emphasis\">" + date + "</span></label>");

    rid = startHash.split("=")[1];
    index = 0;
    while (rid != routesarray[index]["rid"]) {
      index++;
    }

    if (routesarray[index]["state"]) {
      var state = routesarray[index]["state"];
      $('#status').text(state);
      $('#status').css("display", "block");
      if (state == 'New') {
	$('#status').addClass("green-text");
      } else {
	$('#status').addClass("red-text");
      }
    }
    
    $("#hold").attr("src", "https://www.kletterzentrum.com/" + routesarray[index]["imgurl"]);
    $("#hold_caption").text(routesarray[index]["color"]);

    if (routesarray[index]["typ"] == "Bould") {
      $("#lead").attr("src", "images/boulder.png");
      $("#lead").css("width", "190px");
      $("#lead_caption").text("Boulder");
    } else {
      if (routesarray[index]["belay"].indexOf("Lead") != -1) {
	$("#lead").attr("src", "images/lead.png");
	$("#lead").css("width", "190px");
	$("#lead_caption").text("Lead");
      }
      if (routesarray[index]["belay"].indexOf("Toprope") != -1 || routesarray[index]["belay"].indexOf("Toppas") != -1) {
	$("#toprope").attr("src", "images/toppas.png");
	$("#toprope").css("width", "190px");
	$("#toprope_caption").text("Toprope");
      }
    }

    $('#number').html("#" + routesarray[index]["number"]);
    $('#name').html(routesarray[index]["name"]);
    $('#grade').html(routesarray[index]["grade"]);
    $('#grade').addClass(getColorFromGrade(routesarray[index]["grade"], routesarray[index]["typ"]));
    $('#date_and_setter').html(routesarray[index]["date"] + ",  " + routesarray[index]["setter"]);

    if (routesarray[index]["kids"]) {
      $('#kids').html("KIDS");
    }

    var filename = "images/map-images/";

    sector = routesarray[index]["sector"];
    var sub_sector = sector.replace(/,?\s+/g , "-").toLowerCase();
    sub_sector = replaceSpecialLetters(sub_sector);
    
    if (routesarray[index]["place"] == "Gas") {
      $('#sector').text("Gaswerk, " + sector);

      if (routesarray[index]["typ"] == "Bould") {
	sub_sector = sub_sector.split('-').slice(0,2).join('-');
      } else {
	if (sector.indexOf("Halle") != -1) {
	  sub_sector = sub_sector.split('-').slice(2).join('-');
	} else {
	  sub_sector = sub_sector.split('-').slice(1).join('-');
	}
      }
      filename += "gaswerk_" + sub_sector + ".png";
    } else {
      $('#sector').text("Milandia, " + sector);
      filename += "milandia_" + sub_sector + ".png";
    }
    $("#map").attr("src", filename);
    $("#map_link").attr("href", filename);

    $("#route_root").show();
  }
} );

