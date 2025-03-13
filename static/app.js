$(document).ready(function () {
    function loadProduct() {
        $.getJSON("/api/get_product", function (data) {
            if (data.error) {
                alert("No matching product found.");
                return;
            }

            $("#id_match").text(data.id_match);
            $("#off_name").text(data.off_name || "");
            $("#fdc_name").text(data.fdc_name || "");
            $("#off_ingredients").text(data.off_ingredients || "");
            $("#fdc_ingredients").text(data.fdc_ingredients || "");
            $("#off_calories").text(data.off_calories || "");
            $("#fdc_calories").text(data.fdc_calories || "");

            $(".copy-check").prop("checked", false);
            $("input[type='text']").val("");
        });
    }

    $(".copy-check").change(function () {
        if ($(this).is(":checked")) {
            let target = $(this).data("target");
            let source = $(this).data("source");
            $("#result_" + target).val($("#" + source).text());
        }
    });

    $("#mergeBtn").click(function () {
        let mergedProduct = {
            id_match: $("#id_match").text(),
            name: $("#result_name").val(),
            ingredients: $("#result_ingredients").val(),
            calories: $("#result_calories").val()
        };

        $.ajax({
            url: "/api/merge",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(mergedProduct),
            success: function (response) {
                alert(response.message);
                loadProduct();
            }
        });
    });

    loadProduct();
});
