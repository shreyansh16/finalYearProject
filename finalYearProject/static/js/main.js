// JavaScript Document

/*Profile picture upload*/
$('#customFile').on("change",function() {
      console.log("change fire");
     var i = $(this).prev('label').clone();
      var file = $('#customFile')[0].files[0].name;
   console.log(file);
      $(this).prev('label').text(file);

    });