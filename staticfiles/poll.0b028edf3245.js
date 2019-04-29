

 $(document).ready(function () {
   $("input[name='Person']").change(function () {
      var maxAllowed = 2;
      var cnt = $("input[name='Person']:checked").length;
      if (cnt > maxAllowed) 
      {
         $(this).prop("checked", "");
         alert('Select maximum ' + maxAllowed + ' people!');
     }
  });
});