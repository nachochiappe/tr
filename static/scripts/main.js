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
			var cantidad_especialidades = data['especialidades'].length;
			for (var i = 0; i < cantidad_especialidades; i++) {
				$(lista_especialidades).append('<option>' + data['especialidades'][i]['nombre'] + '</option>');
				$(lista_especialidades).append('<input type="hidden" name="' + data['especialidades'][i]['nombre'] + '" value="' + data['especialidades'][i]['id'] + '">');
			}
			obtenerMedicos();
		}
	});
});

$(document).on('change', '#FormControlSelectEspecialidad', function() {
	obtenerMedicos();
});

function obtenerMedicos() {
	$("#FormControlSelectMedico").html('');
	especialidad_seleccionada = $('#FormControlSelectEspecialidad option:selected').text();
	id = $('input[name=' + especialidad_seleccionada + ']').val();
	$.ajax({
		url: '/ajax/obtener_medicos/' + id,
		type: "GET",
		success: function(data) {
			var lista_medicos = document.getElementById('FormControlSelectMedico');
			var cantidad_medicos = data['medicos'].length;
			for (var i = 0; i < cantidad_medicos; i++) {
				$(lista_medicos).append('<option>' + data['medicos'][i]['apellido'] + ', ' + data['medicos'][i]['nombre'] + '</option>');
				$(lista_medicos).append('<input type="hidden" name="' + data['medicos'][i]['apellido'] + data['medicos'][i]['nombre'] + '" value="' + data['medicos'][i]['dni'] + '">');
			}
		}
	});	
}

$(document).on('click', '.ibtnDerivar', function() {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // Estos métodos HTTP no requieren protección CSRF
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	id_paciente = $('input[name=id_paciente]').val();
	medico_seleccionado = $('#FormControlSelectMedico option:selected').text();
	medico_seleccionado = medico_seleccionado.replace(', ', '');
	id_medico = $('input[name=' + medico_seleccionado + ']').val();
	$.ajax({
		url: '/ajax/derivar_paciente/',
		type: "POST",
		data: {
			'id_paciente': id_paciente,
			'id_medico': id_medico,
		},
		beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
		success: function(data) {
			$("#derivar_modal_body").append('<div class="alert alert-success alert-dismissible fade show" role="alert">Paciente derivado.<button type="button" class="close" data-dismiss="alert" aria-label="Cerrar"><span aria-hidden="true">&times;</span></button></div>');
		}
	});
});