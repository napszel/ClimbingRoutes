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
  [',', '-'],
  ['(', '-'],
  [' ', '-'],
  ['#', ''],
  [')', '']
];

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(str, find, replace) {
    return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}

function replaceSpecialLetters(text) {
  for (var i=0; i<special_letters.length; i++) {
    text = replaceAll(text, special_letters[i][0], special_letters[i][1]);
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
      // Show all routes
      "pageLength": -1,
      // Remove pagination
      "paging": false,
      // Order by date column
      "order": [6, "desc"],
      // Define column widths
      "bAutoWidth": false,
      "columnDefs": [
	{ "width": "20px", "targets": [ "twenty" ] },
	{ "width": "40px", "targets": [ "fourty" ] },
	{ "width": "60px", "targets": [ "sixty" ] },
	{ "width": "90px", "targets": [ "ninety" ] },
	{ "width": "110px", "targets": [ "hundredten" ] },
	{ "width": "200px", "targets": [ "twohundred" ] },
	// Hide some columns by default
	{ "visible": false, "targets": [5, 9, 11, 12, 13, 14] },
      ],
      "dom": 'iBrt',
      "buttons": [
	{
	  extend: 'colvis',
	  collectionLayout: 'fixed two-column',
	  postfixButtons: [
	    'colvisRestore'
	  ],
	  columnText: function (dt, idx, title) {
	    if (title == "Sum") {
	      return "Sum of comments";
	    } else {
	      return title;
	    }
          }
	}
      ],
      "oLanguage": {
        "buttons": {
          "colvis": 'Hide columns',
        },
	"sInfo": "",
	"sInfoFiltered": "_TOTAL_ routes found (out of _MAX_)",
	"sInfoEmpty": "",
	"sZeroRecords": "No such route",
      },
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
      if (place == 'mil') {
	place = "Milandia";
      } else {
	place = "Wädenswil";
      }
    }
    if (type == 'bould') {
      type = "Boulder";
    } else {
      type = "Sport";
    }
    $("#title-div").append("<label class=\"title\"><span class=\"emphasis\">" + type + "</span> route <span class=\"emphasis\">#" + number + "</span> of <span class=\"emphasis\">" + place + "</span> set on <span class=\"emphasis\">" + date + "</span></label>");

    rid = startHash.split("=")[1];
    index = 0;
    while (rid != routesarray[index]["pk"]) {
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

    var color_codes = routesarray[index]["color_codes"].split(" ")
    // 'radial-gradient(red 0% 25%, blue 25% 50%, yellow 50% 75%, green 75% 100%)'
    var gradient = "radial-gradient("
    var i;
    for (i = 0; i < color_codes.length; i++) {
      gradient += color_codes[i] + " " + (100 / color_codes.length) * i + "%, ";
      gradient += color_codes[i] + " " + (100 / color_codes.length) * (i+1) + "%, ";
    }
    gradient = gradient.slice(0, -2) + ")";
    $("#hold").css('background-image', gradient);

    $("#hold_caption").text(routesarray[index]["color"]);

    if (routesarray[index]["typ"] == "Bould") {
      $("#lead").attr("src", "images/boulder.png");
      $("#lead").css("width", "190px");
      $("#lead_caption").text("Boulder");
    } else {
      $("#lead").attr("src", "images/lead.png");
      $("#lead").css("width", "190px");
      $("#lead_caption").text("Sport");
      if (routesarray[index]["belay"].indexOf("Toprope") != -1 || routesarray[index]["belay"].indexOf("Toppas") != -1) {
	$("#toprope").attr("src", "images/toppas.png");
	$("#toprope").css("width", "190px");
	$("#toprope_caption").text("Toprope");
      }
    }

    if (routesarray[index]["sector_img"] && routesarray[index]["polygon"]) {
      color = color_codes[0];
      if (routesarray[index]["typ"] == "Bould") {
        function t(t) {for(var r=0;r<t.length;r++)t[r][0]=t[r][0]/a,t[r][1]=t[r][1]/a;return str_path=String(t),str_path.replace(/,/g," ")}
        var a=2.7, i=new Image;            
        i.onload=function() {
          img_width=i.width/a,img_height=i.height/a,
            r=Raphael("sector_image", img_width,img_height),
              r.image(i.src,0,0,img_width,img_height),
              path=$.parseJSON(routesarray[index]["polygon"]),
              string_path=t(path);
          var l=r.path("M "+string_path+" Z");
          l.attr("stroke",color),l.attr("stroke-width",3),l.attr("stroke-linejoin","round"),l.attr("fill",color),l.attr("fill-opacity",.3)
        },
        i.src="images/sectors/"+routesarray[index]["sector_img"]

      }
      else {
        function t(t,e){for(var i=0;i<t.length;i++)if(i>0){var o=r.path("M"+t[i-1][0]/a+" "+t[i-1][1]/a+"L"+t[i][0]/a+" "+t[i][1]/a);o.attr("stroke",e),o.attr("stroke-width",2),o.attr("stroke-linejoin","round")}}
        var a=2.7,e=new Image;
        e.onload=function()
        {
            img_width=e.width/a,img_height=e.height/a,
            r=Raphael("sector_image",img_width,img_height),
                r.image(e.src,0,0,img_width,img_height),
                t($.parseJSON(routesarray[index]["polygon"]),color)
        },e.src="images/sectors/"+routesarray[index]["sector_img"]
      }
      $("#sector_caption").text(routesarray[index]["vlsector"]);
    }
    
    $('#number').html("#" + routesarray[index]["number"]);
    if (routesarray[index]["full_name"]) {
      $('#name').html($('<div>').text(routesarray[index]["full_name"]).html());
    } else {
      $('#name').html($('<div>').text(routesarray[index]["name"]).html());
    }
    $('#grade').html(routesarray[index]["grade"]);
    $('#grade').addClass(getColorFromGrade(routesarray[index]["grade"], routesarray[index]["typ"]));
    $('#date_and_setter').html(routesarray[index]["date"] + ",  " + routesarray[index]["setter"]);

    if (routesarray[index]["kids"]) {
      $('#kids').html("KIDS");
    }

    var filename = "images/map-images/";

    sector = ""
    if (routesarray[index]["vlsector"]) {
      sector = routesarray[index]["vlsector"];
    } else {
      sector = routesarray[index]["sector"];
    }

    file_name_sector = replaceSpecialLetters(sector).split(" ").join("-").toLowerCase();

    sector_place = routesarray[index]["place"];
    if (sector_place == "Gas") {
      $('#sector').text("Gaswerk, " + sector);
      filename += "gaswerk_" + file_name_sector + ".png";
    } else {
      if (sector_place == "Mil") {
	$('#sector').text("Milandia, " + sector);
	filename += "milandia_" + file_name_sector + ".png";
      } else {
	$('#sector').text("Wädenswil, " + sector);
	filename += "waedenswil_" + file_name_sector + ".png";
      }
    }

    $("#map").attr("src", filename);
    $("#map_link").attr("href", filename);

    $("#route_root").show();
  }
} );

