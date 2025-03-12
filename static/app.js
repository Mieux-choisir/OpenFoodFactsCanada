$(document).ready(function () {
    let selectedProduct = null;

    function loadTable(collection) {
        $("#productsTable").DataTable().destroy();  // Supprimer l'instance précédente
        $("#productsTable").DataTable({
            processing: true,
            serverSide: true,
            ajax: {
                url: "/api/products",
                data: function (d) {
                    d.collection = collection;
                },
            },
            columns: [
                { data: "id_match" },
                { data: "id_original" },
                { data: "product_name" },
                { data: "brand_name" },
                { data: "category_en" },
                {
                    data: null,
                    render: function (data, type, row) {
                        return `<button class="merge-btn" data-product='${JSON.stringify(row)}'>Select</button>`;
                    },
                },
            ],
        });

        $("#productsTable tbody").on("click", ".merge-btn", function () {
            selectedProduct = $(this).data("product");
            alert(`Selected: ${selectedProduct.product_name}`);
        });
    }

    $("#collectionSelect").change(function () {
        let collection = $(this).val();
        loadTable(collection);
    });

    $("#mergeButton").click(function () {
        if (!selectedProduct) {
            alert("Select a product to merge first!");
            return;
        }

        $.ajax({
            url: "/api/merge",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(selectedProduct),
            success: function (response) {
                alert("Product merged successfully!");
            },
        });
    });

    loadTable("fdc_products");  // Charger par défaut
});
