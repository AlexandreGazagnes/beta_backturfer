

$("#bet_type").on('change', function(){
    $(".select_strats").css("display","none");
    $(".select_" + $(this).val()).css("display","block");
    });



