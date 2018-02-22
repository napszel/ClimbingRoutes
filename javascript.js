$(document).ready(function() {
  // Setup - add a text input to each footer cell
  $('#example tfoot th').each( function () {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="'+title+'" />' );
  } );
  
  // DataTable
  var table = $('#example').DataTable( {
    "pageLength": 50,
    "columnDefs": [
      { "width": "20px", "targets": [ "narrow" ] },
      { "width": "90px", "targets": [ "middle" ] },
      { "width": "35px", "targets": [ "smallish" ] },
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
} );
