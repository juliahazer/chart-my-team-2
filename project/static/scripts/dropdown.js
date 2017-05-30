$(function(){
  var $selectSeason = $('#selectSeason');
  var $selectLeague = $('#selectLeague');
  var $selectTeam = $('#selectTeam');
  var $svgTag = $('#svgTag');

  var $seasonSelectDiv = $('#seasonSelectDiv');
  var $leagueSelectDiv = $('#leagueSelectDiv');
  var $teamSelectDiv = $('#teamSelectDiv');

  var baseUrl = window.location.protocol + "//" + window.location.host + "/";

  var teamId = null;
  var leagueId = null;
  var seasonId = null;

  //set team id if on show page
  if ($svgTag.length){
    teamId = Number($svgTag.attr('data-team-id'));
    leagueId = Number($svgTag.attr('data-league-id'));
    seasonId = Number($svgTag.attr('data-season-id'));
  }

  $.ajax({
    method: "GET",
    url: baseUrl + "seasons/json",
    dataType: "json"
  }).then(function(data){
    data.map(function(el){
      var selected = "";
      if (seasonId === el.id){
        selected = " selected"
      }  
      $selectSeason.append(`<option value="${el.id}"${selected}>
            ${el.year} ${el.name}
        </option>`);
    });
  }); 

  if (teamId !== null){
    $.ajax({
      method: "GET",
      url: baseUrl + "seasons/" + seasonId + "/json"
    }).then(function(data){
      $teamSelectDiv.addClass('hidden');
      //first empty the select
      $selectLeague.find('option').remove(); 
      $selectLeague.append("<option disabled selected value> -- select an option -- </option>");

      if (data.length !== 0){
        data.map(function(el){
          var selected = "";
          if (leagueId === el.id){
            selected = " selected"
          }  
          $selectLeague.append(`<option value="${el.id}"${selected}>
              ${el.name}
            </option>`);
        });
        $leagueSelectDiv.removeClass('hidden');
      } else {
        $leagueSelectDiv.addClass('hidden');
      }
    });

    $.ajax({
      method: "GET",
      url: baseUrl + "leagues/" + leagueId + "/json"
    }).then(function(data){
      //first empty the select
      $selectTeam.find('option').remove();
      $selectTeam.append("<option disabled selected value> -- select an option -- </option>"); 

      if (data.length !== 0){
        data.map(function(el){
          var selected = "";
          if (teamId === el.id){
            selected = " selected"
          }  
          $selectTeam.append(`<option value="${el.id}"${selected}>
            ${el.name}
        </option>`);
        });
        $teamSelectDiv.removeClass('hidden');
      } else {
        $teamSelectDiv.addClass('hidden');
      }
    });
  }

  /********************* EVENT LISTENERS ***********************/
  $selectSeason.on('change', function(){
    var seasonId = $(this).val();
    $.ajax({
      method: "GET",
      url: baseUrl + "seasons/" + seasonId + "/json"
    }).then(function(data){
      $teamSelectDiv.addClass('hidden');
      //first empty the select
      $selectLeague.find('option').remove(); 
      $selectLeague.append("<option disabled selected value> -- select an option -- </option>");

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

  $selectLeague.on('change', function(){
    var leagueId = $(this).val();
    $.ajax({
      method: "GET",
      url: baseUrl + "leagues/" + leagueId + "/json"
    }).then(function(data){
      //first empty the select
      $selectTeam.find('option').remove();
      $selectTeam.append("<option disabled selected value> -- select an option -- </option>"); 

      if (data.length !== 0){
        data.map(function(el){
          $selectTeam.append(`<option value="${el.id}">
            ${el.name}
        </option>`);
        });
        $teamSelectDiv.removeClass('hidden');
      } else {
        $teamSelectDiv.addClass('hidden');
      }
    });
  });

  $selectTeam.on('change', function(){
    var teamId = $(this).val();
    window.location.href = baseUrl + "teams/" + teamId;
  });

})