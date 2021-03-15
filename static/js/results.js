
  var idc=JSON.parse("{{jsonidc|escapejs}}");
for (var key in idc.title) {
  var size=idc.title[key][1]['nohtml'].length
  if(size>70){
    document.getElementById('linesl-title '+key+' warn').innerHTML="Warning: too many characters: ( "+size+" ), not everything will apear in google, limit it at 70";
  }
}
console.log()
for (var key in idc.description) {
  var size=idc.description[key][1]['nohtml'].length
  if(size>150){
    document.getElementById('linesl-description '+key+' warn').innerHTML="Warning: too many characters: ( "+size+" ), not everything will apear in google, limit it at 150";
  }
}
  function change(id, arrow){
    var html=document.getElementById('h-'+id).checked;
    var detail=document.getElementById(id).hasAttribute("open");
    if (arrow){
      detail=!detail;
    }
    if(html){
      var x=document.getElementsByClassName('linesh-'+id);
      var y=document.getElementsByClassName('linesl-'+id);
    }else{
      var x=document.getElementsByClassName('linesl-'+id);
      var y=document.getElementsByClassName('linesh-'+id);
    }
    var n=document.getElementsByClassName('liness-'+id);
    for(var i=0; i<x.length; i++){
      if (!detail){
        x[i].style.display='none';
        y[i].style.display='none';
      }
      else{
        x[i].style.display='block';
        y[i].style.display='none';
      }
    }
    for(var i=0; i<n.length; i++){
      if (!detail){
        n[i].style.display='block';
      }else{
        n[i].style.display='none';}
    }
}
function change_single(id){
  var html=document.getElementById('h-'+id).checked;
  if(html){
    var x=document.getElementsByClassName('linesh-'+id);
    var y=document.getElementsByClassName('linesl-'+id);
  }else{
    var x=document.getElementsByClassName('linesl-'+id);
    var y=document.getElementsByClassName('linesh-'+id);
  }

  for(var i=0; i<x.length; i++){
    x[i].style.display='block';
    y[i].style.display='none';
  }

}
