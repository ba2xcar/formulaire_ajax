$( document ).ready(function() {
   $('#fil').change(function(){ 
      var x = document.getElementById("fil").value;
      $('#classe').children('option:not(:first)').remove();
      $('#mont_ins').val("");
      $('#mensualite').val("");
      $('#total_ins').val("");
      /*document.getElementById("response").innerHTML = "You selected: " + x;*/
      $.ajax({ 
         type: "GET",
         url: "http://127.0.0.1:5000/filiere&"+x,
      });
   });
});

$( document ).ready(function() {
   $('#fil').change(function(){ 
      var x = document.getElementById("fil").value;
      $.ajax({ 
         type: "GET",
         contentType: 'application/json; charset=utf-8',
         url: "http://127.0.0.1:5000/filiere&"+x,
         success: function(liste_classe){
            $('#classe').children('option:not(:first)').remove();
            $.each(liste_classe,function(index,d){
               /* $('#fil').append('Prénom : ' + d.Prenom); */         
               /* var selection = document.getElementById("classe");
               selection.options[selection.options.length] = new Option(d.libelle, d.id);*/   
               $("#classe").append("<option value="+ d.id +">" + d.libelle + "</option>");
            });
         }
      });
   });
});

 /********************************AJAX CLASSE****************************/
$( document ).ready(function() {
   $('#classe').change(function(){ 
      var x = document.getElementById("classe").value;
      $('#mont_ins').val("");
      $('#mensualite').val("");
      $('#total_ins').val("");
/*                document.getElementById("response").innerHTML = "You selected: " + x;
*/    $.ajax({ 
         type: "GET",
         url: "http://127.0.0.1:5000/classe&"+x,
      });
   });
});

$( document ).ready(function() {
   $('#classe').change(function(){ 
      var x = document.getElementById("classe").value;
      $.ajax({ 
         type: "GET",
         contentType: 'application/json; charset=utf-8',
         url: "http://127.0.0.1:5000/classe&"+x,
         success: function(liste_ele_classe){
            $.each(liste_ele_classe,function(index,d){
               $('#mont_ins').val(d.mont_ins);
               $('#mensualite').val(d.mensualite);
               $('#total_ins').val(d.mont_ins+d.mensualite);    
            });
         }
      });
   });
});
/*********************************************ACTION BOUTON RADIO****************************/
$(function() {
   var matricule = document.getElementById("mat").value;
   $('#ancien').on('click',function(){
      document.getElementById("text-radio").innerHTML = "REINSCRIPTION";
      $('#fil').children('option:not(:first)').remove();
      $('#mat').attr('readonly', false); 
      $('#mat').val(""); 
      vider();
      lire(); 

      changeColor();

   
         
   }); 
   $('#nouveau').on('click',function(){
      document.getElementById("text-radio").innerHTML = "INSCRIPTION";

      $('#mat').attr('readonly', true);
      $('#mat').val(matricule);
      window.location.reload();
          
   });        
});

/*******************************************SEARCH APPRENANT******************** */

function ecouteInput(event) {
   var x = window.event.which || window.event.keyCode;
   if(x==13){
      document.getElementById('boutonenvoi').disabled = true;
      var searchmat = document.getElementById("mat").value;
      $.ajax({ 
         type: "GET",
         url: "http://127.0.0.1:5000/search&"+searchmat,
      });
      $.ajax({ 
         type: "GET",
         contentType: 'application/json; charset=utf-8',
         url: "http://127.0.0.1:5000/search&"+searchmat,

         success: function(apprenant_find){
            
            $.each(apprenant_find, function(index,d){
               if(d.prenom){
                  /*document.getElementById("response").innerHTML = "You selected is pliein";*/
                  $('#prenom').val(d.prenom);

                  $('#nom').val(d.nom);
                  $('#sexe').val(d.sexe);
                  
                  $('#date_naissance').val(convert(d.date_naiss));
                  $('#lieu_naissance').val(d.lieu_naiss);
                  $('#adresse').val(d.adresse);
                  $('#email').val(d.email);
                  $('#telephone').val(d.tel); 
                  $("#fil").append("<option value="+ d.id_fil +">" + d.nom_fil + "</option>");

                  $('#mat').attr('readonly', true);
                  lire();
                  document.getElementById('boutonenvoi').disabled = false;

                  document.getElementById('boutsearch').style.display = 'block';

               }
               else{
                  $.uiAlert({
                     textHead: d.vide,
                     text: '', // Text
                     bgcolor: '#DB2828', // background-color
                     textcolor: '#fff', // color
                     position: 'top-center',// position . top And bottom ||  left / center / right
                     time: 1, // time
                  })                  
               }
            });
         },
      });
   }
}

$('#boutsearch').on('click',function(){
   document.getElementById('boutsearch').style.display = 'none';
   $('#mat').attr('readonly', false);
   $('#mat').val("");

   vider();

});

/*************************************************CONTROLE CHAMP*****************************/



newFunction();
function newFunction() {
   $('.ui.form')
   .form({
      fields: {
         prenom: 'empty',
         nom: 'empty',
         sexe: 'empty',
         date_naissance: 'empty',
         lieu_naissance: 'empty',
         adresse: 'empty',
         email: 'empty',
         telephone: 'empty',
         promo: 'empty',
         fil : 'empty',
         classe : 'empty',
         date_ins : 'empty',
      }
   });
}

/*********************************************LES FONCTIONS***********************/
function convert(str) {
   var date = new Date(str),
      mnth = ("0" + (date.getMonth() + 1)).slice(-2),
      day = ("0" + date.getDate()).slice(-2);
   return [date.getFullYear(), mnth, day].join("-");
}
function lire(){
   $('#prenom').attr('readonly', true);
   $('#nom').attr('readonly', true);
   document.getElementById('sexe').disabled=true
   $('#date_naissance').attr('readonly', true);
   $('#lieu_naissance').attr('readonly', true);
   $('#adresse').attr('readonly', true);
   $('#email').attr('readonly', true);
   $('#telephone').attr('readonly', true);
}
function ecrire(){
   $('#prenom').attr('readonly', false);
   $('#nom').attr('readonly', false);
   document.getElementById('sexe').disabled=false
   $('#date_naissance').attr('readonly', false);
   $('#lieu_naissance').attr('readonly', false);
   $('#adresse').attr('readonly', false);
   $('#telephone').attr('readonly', false);
   document.getElementById('boutsearch').style.display = 'none';

}
function vider(){
      $('#prenom').val("");
      $('#nom').val("");
      $('#sexe').val("");
      $('#date_naissance').val("");
      $('#lieu_naissance').val("");
      $('#adresse').val("");
      $('#email').val("");
      $('#telephone').val("");        
      $('#fil').val("");
      $('#classe').val("");
      $('#mont_ins').val("");
      $('#mensualite').val("");
      $('#total_ins').val(""); 
      $('#date_ins').val("");
}

function changeColor(){

   var x = document.getElementsByClassName("champ");
   var y = document.getElementsByClassName("lab");
   for (var i=0 ; i < x.length ; i++) {
      x[i].style.borderColor = "#dfe0e0";
      x[i].style.backgroundColor = "white";
   }
   for (var j=0 ; j < y.length ; j++) {      
      y[j].style.color="black";
   }

}