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
            cols += '<td><input type="text" class="form-control form-control-sm" name="posologia" form="form_medicamento"/></td>';
            cols += '<td></td>';
            cols += '<td><input type="text" class="form-control form-control-sm" name="fecha_inicio" form="form_medicamento"/></td>';
            cols += '<td><input type="text" class="form-control form-control-sm" name="fecha_fin" form="form_medicamento"/></td>';
            cols += '<td></td>';

            cols += '<td><input type="submit" class="ibtnSav btn btn-sm btn-success" value="Guardar" form="form_medicamento">';
            cols += '<input type="button" class="ibtnDel btn btn-sm btn-danger" value="Borrar"></td>';
            newRow.append(cols);
            $("table.table-sm.table-hover").append(newRow);
        }
    });

    $("table.table-sm.table-hover.medact").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        $("#addrow").removeClass('disabled');
    })
        .on("click", ".ibtnSav", function (event) {

        $("#addrow").removeClass('disabled');
    });

    $(function() {
        $("input[name^=fecha_inicio]").datepicker({dateFormat: 'yyyy-mm-dd'});
        $("input[name^=fecha_fin]").datepicker({dateFormat: 'yyyy-mm-dd'});
    });
});