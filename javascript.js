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
      "order": [6, 'desc'],
      "pageLength": -1,
      "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
      "columnDefs": [
	{ "width": "20px", "targets": [ "twenty" ] },
	{ "width": "40px", "targets": [ "fourty" ] },
	{ "width": "60px", "targets": [ "sixty" ] },
	{ "width": "90px", "targets": [ "ninety" ] },
	{ "width": "110px", "targets": [ "hundredten" ] }
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
    $("#header").append("<h2>Comments for <span style=\"color: #ff0000\">" + type + "</span> route <span style=\"color: #ff0000\">#" + number + "</span> of <span style=\"color: #ff0000\">" + place + "</span> set on <span style=\"color: #ff0000\">" + date + "</span></h2>");
    $("#route_root").show();
  }
} );

