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
*/               $.ajax({ 
          type: "GET",
          url: "http://127.0.0.1:5000/classe&"+x,
       });
    });
 });

 $( document ).ready(function() {
    $('#classe').change(function(){ 
       var x = document.getElementById("classe").value;
/*                document.getElementById("response").innerHTML = x;
*/
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

        $('#mat').attr('readonly', false); 
        $('#mat').val(""); 
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
    }); 
    $('#nouveau').on('click',function(){
        document.getElementById("text-radio").innerHTML = "INSCRIPTION";

        $('#mat').attr('readonly', true);
        $('#mat').val(matricule);
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
        
    });        
 });