$(function(){
  var $selectSeason = $('#selectSeason');
  var $selectLeague = $('#selectLeague');
  var $selectTeam = $('#selectTeam');

  var $seasonSelectDiv = $('#seasonSelectDiv');
  var $leagueSelectDiv = $('#leagueSelectDiv');
  var $teamSelectDiv = $('#teamSelectDiv');

  var baseUrl = window.location.protocol + "//" + window.location.host + "/";

  $.ajax({
    method: "GET",
    url: baseUrl + "seasons/json",
    dataType: "json"
  }).then(function(data){
    data.map(function(el){
      $selectSeason.append(`<option value="${el.id}">
          ${el.year} ${el.name}
      </option>`);
    });
  }); 



  /********************* EVENT LISTENERS ***********************/
  $selectSeason.on('change', function(){
    var seasonId = $(this).val();
    $.ajax({
      method: "GET",
      url: baseUrl + "seasons/" + seasonId + "/json"
    }).then(function(data){
      //first empty the select
      $selectLeague.find('option').remove(); 

      if (data.length !== 0){
        data.map(function(el){
          $selectLeague.append(`<option value="${el.id}">
            ${el.name}
        </option>`);
        });
        $leagueSelectDiv.removeClass('hidden');
      } else {
        $leagueSelectDiv.addClass('hidden');
      }
    });

  });

})