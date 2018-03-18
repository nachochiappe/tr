// FUNCIONES DE TOMAR MEDICACIÓN

$(document).on('click','.ibtnTomar', function(){
	var str = event.target.id;
	var id = parseInt(str.replace('tomar-', ''));
	tomar_medicacion(id);
});

function tomar_medicacion(id) {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // Estos métodos HTTP no requieren protección CSRF
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajax({
		url: '/ajax/tomar_medicacion/',
		type: "POST",
		data: {
			'id': id,
		},
		beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
		success: function(data) {
			var valorActual = parseInt($("#dosis-completadas-"+id).html());
		    $("#dosis-completadas-"+id).html(valorActual + 1);
		}
	});
}

// FUNCIONES DE BORRAR MEDICAMENTO

$(document).off('click', '.ibtnBorrar').on('click', '.ibtnBorrar', function() {
	var itemactual = $(this);
	var str = event.target.id;
	var id = parseInt(str.replace('borrar-', ''));
	$(document).off('click', '.btn-confirmar').on('click','.btn-confirmar', function() {
		$("#medicamentoModal").modal('hide');
		borrar_medicamento(itemactual, id);
	});
});

function borrar_medicamento(itemactual, id) {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // Estos métodos HTTP no requieren protección CSRF
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajax({
		url: '/ajax/borrar_medicamento/',
		type: "POST",
		data: {
			'id': id,
		},
		beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
		success: function(data) {
			itemactual.closest('tr').remove();
		}
	});
};

// FUNCIONES DE DERIVAR PACIENTE

$(document).one('click', '.derivar-paciente', function() {
	$.ajax({
		url: '/ajax/obtener_especialidades/',
		type: "GET",
		success: function(data) {
			var lista_especialidades = document.getElementById('FormControlSelectEspecialidad');
			for (var i = 0; i < 2; i++) {
				$(lista_especialidades).append('<option>' + data['especialidades'][i]['nombre'] + '</option>');
			}
			id = data['especialidades'][0]['id'];
			$.ajax({
				url: '/ajax/obtener_medicos/' + id,
				type: "GET",
				success: function(data) {
					var lista_medicos = document.getElementById('FormControlSelectMedico');
					for (var i = 0; i < 1; i++) {
						$(lista_medicos).append('<option>' + data['medicos'][i]['apellido'] + ', ' + data['medicos'][i]['nombre'] + '</option>');
					}
				}
			});
		}
	});
});
