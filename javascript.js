$(document).ready(function() {
  var startHash = window.location.search;
  if (!startHash) {
    $("#main_table").show();
    
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
      var title = $(this).text();
      $(this).html( '<input type="text" placeholder="'+title+'" />' );
    } );
    
    // DataTable
    var table = $('#example').DataTable( {
      "order": [7, 'desc'],
      "pageLength": -1,
      "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
      "columnDefs": [
	{ "width": "20px", "targets": [ "twenty" ] },
	{ "width": "40px", "targets": [ "fourty" ] },
	{ "width": "60px", "targets": [ "sixty" ] },
	{ "width": "90px", "targets": [ "ninety" ] },
	{ "width": "110px", "targets": [ "hundredten" ] },
	{ "visible": false, "targets": [6, -1, -4] }
      ],
      "dom": 'ifBrt',
      "buttons": [
        'colvis'
      ]
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

    $('#number').html("#" + routesarray[index]["number"]);
    $('#name').html(routesarray[index]["name"]);
    $('#grade').html(routesarray[index]["grade"]);
    $('#date_and_setter').html(routesarray[index]["date"] + ",  " + routesarray[index]["setter"]);

    if (routesarray[index]["kids"]) {
      $('#kids').html("KIDS");
    }

    $("#route_root").show();
  }
} );

