$(function(){

  var $tableScorecards = $('#tableScorecards')
      $tableScorecards.DataTable({
      'paging': true,
      'scrollX': false,
      "columnDefs": [
        { "orderable": false, "targets": 3 }
      ]
    });

});