function ecrire() {
   $('#prenom').attr('readonly', false);
   $('#nom').attr('readonly', false);
   document.getElementById('sexe').disabled = false;
   $('#date_naissance').attr('readonly', false);
   $('#lieu_naissance').attr('readonly', false);
   $('#adresse').attr('readonly', false);
   $('#telephone').attr('readonly', false);
   document.getElementById('boutsearch').style.display = 'none';
}
