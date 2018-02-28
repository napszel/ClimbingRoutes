$(document).ready(function() {
  var startHash = window.location.search;
  if (!startHash) {
    $("#main_table").show();
    
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
      var title = $(this).text();
      if (title) {
	$(this).html( '<input type="text" placeholder="'+title+'" />' );
      } else {
	$(this).html( '<label style="font-size: 9px">comments</label>' );
      }
    } );
    
    // DataTable
    var table = $('#example').DataTable( {
      "pageLength": -1,
      "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
      "columnDefs": [
	{ "width": "20px", "targets": [ "narrow" ] },
	{ "width": "90px", "targets": [ "middle" ] },
	{ "width": "35px", "targets": [ "smallish" ] },
	{ searchable: false, orderable: false, targets: [4] },
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

