 function task_predict() {

 	$.ajax({
 		url: '/tasks/predict/',
 		type: "POST",
 		data: { 
 			'time': $('#hours').val(),
 			'csrfmiddlewaretoken': jQuery("[name=csrfmiddlewaretoken]").val(),
 		},
 		contentType: "application/json",
 		dataType: "json",
 		success: function(data){
 			console.log("Here we go!");
 			$("#hours").notify(returned_data, "success");
 		},
 		error: function(ts){
 			console.log(ts);
 		}
 	});

 }