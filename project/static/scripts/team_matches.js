$(function(){

  var $tableMatches = $('#tableMatches')
  var $tbody = $('#tableBody');

  var baseUrl = window.location.protocol + "//" + window.location.host + "/";
  var currUrl = window.location.href;

  var matchArr = [];

  $.ajax({
    method: "GET",
    url: currUrl + "_json",
    dataType: "json"
  }).then(function(data){
    matchArr = data;
    console.log(matchArr)
    writeTable();
  });

  function writeTable(){
    $tbody.empty()
    // if (sortKind === 'sort'){
    //   if (sortValue === 'asc'){
    //     if (sortField === 'date'){
    //       currArr.sort(function(a,b){
    //         return new Date(a.date) - new Date(b.date);
    //       })
    //     } else {
    //       currArr.sort(function(a,b){
    //         return a[sortField] - b[sortField]
    //       });
    //     }
    //   } else {
    //     if (sortField === 'date'){
    //       currArr.sort(function(a,b){
    //         return new Date(b.date) - new Date(a.date);
    //       })
    //     } else {
    //       currArr.sort(function(a,b){
    //         return b[sortField] - a[sortField]
    //       });
    //     }
    //   }
    // } else if (sortKind === 'filter' && sortValue !== 'all') { //filter
    //   currArr = currArr.filter(function(el){
    //     return el[sortField] === sortValue;
    //   })
    // }
    matchArr.map(function(el, i){
      var tbody_html = `
        <tr data-id='${el.id}'`;
      if (el.winner === 'Team'){
        tbody_html += `class='success'`;
      } else {
        tbody_html += `class='danger'`;
      }
      tbody_html += `>
          <td>${el.date}</td>
          <td>
            <a href='${baseUrl}teams/${el.opponent_id}/matches'>
              ${el.opponent}
            </a>
          </td>
          <td>${el.type}</td>
          <td>${el.line}</td>
          <td>${el.team_player_1}`;

      if (el.type == 'doubles'){
        tbody_html += ` /<br>${el.team_player_2}`;
      }

      tbody_html +=`</td>
          <td>${el.opp_player_1}`;

      if (el.type == 'doubles'){
        tbody_html += ` /<br>${el.opp_player_2}`;
      }
          
      tbody_html +=`</td>
          <td>${el.winner}</td>
          <td>${el.winning_score}</td>
          <td>${el.location}</td>
          <td>
            <a href="//www.ustanorcal.com/scorecard.asp?id=${el.scorecard_id}" target="_blank">
              Link
            </a>
          </td>
        </tr>`
      $tbody.append(tbody_html);
    });
    $tableMatches.DataTable({
      'paging': true
    });
  }
 


  /********************* EVENT LISTENERS ***********************/
  // $selectDate.on('change', function(){
  //   var val = $(this).val();
  //   //reset first all menus to 1st option
  //   $('select').not(this).find('option:eq(0)').prop('selected', true);
  //   writeTable('date', val, 'sort');
  // });

  // $selectType.on('change', function(){
  //   var val = $(this).val();
  //   //reset first all menus to 1st option
  //   $('select').not(this).find('option:eq(0)').prop('selected', true);
  //   writeTable('type', val, 'filter');
  // });

  // $selectWinner.on('change', function(){
  //   var val = $(this).val();
  //   //reset first all menus to 1st option
  //   $('select').not(this).find('option:eq(0)').prop('selected', true);
  //   writeTable('winner', val, 'filter');
  // });

  // $selectLocation.on('change', function(){
  //   var val = $(this).val();
  //   //reset first all menus to 1st option
  //   $('select').not(this).find('option:eq(0)').prop('selected', true);
  //   writeTable('location', val, 'filter');
  // });

})

