$(document).ready(function() {
  var startHash = window.location.search;
  if (!startHash) {
    $("#main_table").show();
    
    // Setup - add a text input to each footer cell -> search boxes for each column
    // - also create the array with default searches
    var default_search_values = []
    $('#example tfoot th').each( function () {
      var placeholder = $(this)[0].attributes['placeholder'].value;
      var default_value = ""
      if ($(this)[0].attributes['default']) {
	default_value = $(this)[0].attributes['default'].value;
	default_search_values.push({"sSearch": default_value});
      } else {
	default_search_values.push(null);
      }
      $(this).html( '<input type="text" placeholder="'+placeholder+'" value="'+default_value+'"/>' );
    } );
    
    // DataTable
    var table = $('#example').DataTable( {
      "order": [5, 'desc'],
      "pageLength": -1,
      "paging": false,
      "bAutoWidth": false,
      "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
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
      
      $( 'input', this.footer() ).on( 'keyup change', function () {
	if ( that.search() !== this.value ) {
          that
            .search( this.value )
            .draw();
	}
      } );
    } );
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
    $("#header").append("<h2><span style=\"color: #ff0000\">" + type + "</span> route <span style=\"color: #ff0000\">#" + number + "</span> of <span style=\"color: #ff0000\">" + place + "</span> set on <span style=\"color: #ff0000\">" + date + "</span></h2>");

    rid = startHash.split("=")[1];
    index = 0;
    while (rid != routesarray[index]["rid"]) {
      index++;
    }

    if (routesarray[index]["state"]) {
      $('#status').text(routesarray[index]["state"]);
      $('#status').css("display", "block");
    }
    
    $("#hold").attr("src", "http://www.kletterzentrum.com/" + routesarray[index]["imgurl"]);
    $("#hold_caption").text(routesarray[index]["color"]);

    if (routesarray[index]["typ"] == "Bould") {
      $("#lead").attr("src", "boulder.png");
      $("#lead").css("width", "190px");
      $("#lead_caption").text("Boulder");
    } else {
      if (routesarray[index]["belay"].indexOf("Lead") != -1) {
	$("#lead").attr("src", "lead.png");
	$("#lead").css("width", "190px");
	$("#lead_caption").text("Lead");
      }
      if (routesarray[index]["belay"].indexOf("Toprope") != -1 || routesarray[index]["belay"].indexOf("Toppas") != -1) {
	$("#toprope").attr("src", "toppas.png");
	$("#toprope").css("width", "190px");
	$("#toprope_caption").text("Toprope");
      }
    }

    $('#number').html("#" + routesarray[index]["number"]);
    $('#name').html(routesarray[index]["name"]);
    $('#grade').html(routesarray[index]["grade"]);
    $('#date_and_setter').html(routesarray[index]["date"] + ",  " + routesarray[index]["setter"]);

    if (routesarray[index]["kids"]) {
      $('#kids').html("KIDS");
    }

    if (routesarray[index]["place"] == "Gas") {
      sector = routesarray[index]["sector"];
      $('#sector').text("Gaswerk, " + sector);
      if (sector.indexOf("Halle") != -1) {
	halle_no = sector.slice(sector.indexOf("Halle") + 6, sector.indexOf("Halle") + 7);
	$("#map").attr("src", "gaswerk_halle" + halle_no + ".png");
	$("#map_link").attr("href", "gaswerk_halle" + halle_no + ".png");
      } else if (sector.indexOf("Outdoor") != -1) {
	$("#map").attr("src", "gaswerk_outdoor.png");
	$("#map_link").attr("href", "gaswerk_outdoor.png");
      } else if (routesarray[index]["typ"] == "Bould") {
	$("#map").attr("src", "gaswerk_boulder.png");
	$("#map_link").attr("href", "gaswerk_boulder.png");
      } else {
	$("#map").attr("src", "gaswerk_map.png");
	$("#map_link").attr("href", "gaswerk_map.png");
      }
    } else {
      sector = routesarray[index]["sector"];
      $('#sector').text("Milandia, " + sector);
      if (routesarray[index]["typ"] == "Bould") {
	$("#map").attr("src", "milandia_boulder.png");
	$("#map_link").attr("href", "milandia_boulder.png");
      } else {
	$("#map").attr("src", "milandia_" + sector.split(" ")[0].toLowerCase() + ".png");
	$("#map_link").attr("href", "milandia_" + sector.split(" ")[0].toLowerCase() + ".png");
      }
    }

    $("#route_root").show();
  }
} );

