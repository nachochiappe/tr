$.datepicker.regional['es'] = {
 closeText: 'Cerrar',
 prevText: '< Ant',
 nextText: 'Sig >',
 currentText: 'Hoy',
 monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
 monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
 dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
 dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
 dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
 weekHeader: 'Sm',
 dateFormat: 'dd/mm/yy',
 firstDay: 1,
 isRTL: false,
 showMonthAfterYear: false,
 yearSuffix: ''
 };
$.datepicker.setDefaults($.datepicker.regional['es']);

$(document).ready(function () {
    $("#addrow").on("click", function () {
        if($("#addrow").hasClass('disabled')) {
            return;
        }
        else {
            $("#addrow").addClass('disabled');

            var newRow = $("<tr>");
            var cols = "";

            cols += '<th scope="row"><input type="text" class="form-control form-control-sm" name="medicamento" form="form_medicamento"/></th>';
            cols += '<td>Cada' +
                '<input type="text" class="form-control form-control-sm" name="posologia_cantidad" form="form_medicamento" size="1"/>' +
                '<select class="form-control form-control-sm" name="posologia_unidad" form="form_medicamento">' +
                '<option value="horas">Horas</option>' +
                '<option value="dias">Días</option>' +
                '<option value="semanas">Semanas</option>' +
                '<option value="meses">Meses</option></select>' +
                '</td>';
            cols += '<td></td>';
            cols += '<td><input type="text" class="form-control form-control-sm" name="fecha_inicio" form="form_medicamento"/></td>';
            cols += '<td><input type="text" class="form-control form-control-sm" name="fecha_fin" form="form_medicamento"/></td>';
            cols += '<td></td>';

            cols += '<td><input type="submit" class="ibtnSav btn btn-sm btn-success" value="Guardar" form="form_medicamento">';
            cols += '<input type="button" class="ibtnDel btn btn-sm btn-danger" value="Borrar"></td>';
            newRow.append(cols);
            $("table[name^=medvigentes]").append(newRow);
        }
		$(function() {
			$("input[name^=fecha_inicio]").datepicker({dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true});
			$("input[name^=fecha_fin]").datepicker({dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true});
		});
    });

    $("table[name^=medvigentes]").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        $("#addrow").removeClass('disabled');
    })
        .on("click", ".ibtnSav", function (event) {

        $("#addrow").removeClass('disabled');
    });
	
});

