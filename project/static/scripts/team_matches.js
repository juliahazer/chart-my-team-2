$(function(){

  var $tbody = $('#tableBody');
  var $selectDate = $('#selectDate');
  var $selectType = $('#selectType');

  var baseUrl = window.location.protocol + "//" + window.location.host + "/";
  var currUrl = window.location.href;

  var matchArr = [];

  var sortField = null;
  var sortType = null;
  var sortKind = null;


  $.ajax({
    method: "GET",
    url: currUrl + "_json",
    dataType: "json"
  }).then(function(data){
    matchArr = data;
    console.log(matchArr)
    writeTable(sortField, sortType, sortKind);
  });

  function writeTable(sortField, sortValue, sortKind){
    $tbody.empty()
    var currArr = matchArr;
    if (sortKind === 'sort'){
      if (sortValue === 'asc'){
        if (sortField === 'date'){
          currArr.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
          })
        } else {
          currArr.sort(function(a,b){
            return a[sortField] - b[sortField]
          });
        }
      } else {
        if (sortField === 'date'){
          currArr.sort(function(a,b){
            return new Date(b.date) - new Date(a.date);
          })
        } else {
          currArr.sort(function(a,b){
            return b[sortField] - a[sortField]
          });
        }
      }
    } else if (sortKind === 'filter' && sortValue !== 'all') { //filter
      currArr = currArr.filter(function(el){
        return el[sortField] === sortValue;
      })
    }
    currArr.map(function(el, i){
      $tbody.append(`
        <tr data-id='${el.id}'>
          <td>${i}</td>
          <td>${el.date}</td>
          <td>
            <a href='${baseUrl}teams/${el.opponent_id}/matches'>
              ${el.opponent}
            </a>
          </td>
          <td>${el.type}</td>
          <td>${el.line}</td>
          <td>${el.team_player_1}</td>
          <td>${el.team_player_2}</td>
          <td>${el.opp_player_1}</td>
          <td>${el.opp_player_2}</td>
          <td>${el.winner}</td>
          <td>${el.winning_score}</td>
          <td>${el.location}</td>
          <td>
            <a href="//www.ustanorcal.com/scorecard.asp?id=${el.scorecard_id}" target="_blank">
              Link
            </a>
          </td>
        </tr>`
      );
    });
  }
 


  /********************* EVENT LISTENERS ***********************/
  $selectDate.on('change', function(){
    var val = $(this).val();
    writeTable('date', val, 'sort');
  });

  $selectType.on('change', function(){
    var val = $(this).val();
    writeTable('type', val, 'filter');
  });

})

