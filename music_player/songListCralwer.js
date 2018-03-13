var table = document.getElementsByClassName("wiki-table")[1];
var tr_list = table.getElementsByTagName("tr");
var song_list = [];
for (var i = 3; i < tr_list.length; i++) {
  song_list.push(tr_list[i].getElementsByTagName("td")[1].getElementsByTagName("p")[0].innerHTML);
}
console.log(song_list);
