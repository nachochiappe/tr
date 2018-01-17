$(document).ready(function(){
	$('#tomar-medicacion').click(function(){
	    tomar_medicacion();
	});
});

function tomar_medicacion() {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // Estos métodos HTTP no requieren protección CSRF
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajax({
		url: '/ajax/tomar_medicacion/',
		type: "POST",
		data: {
			'id': $('.medicamentoid').val(),
		},
		beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
		success: function(data) {
			var valorActual = parseInt($("#dosis-completadas").html());
		    $("#dosis-completadas").html(valorActual + 1);
		}
	});
}