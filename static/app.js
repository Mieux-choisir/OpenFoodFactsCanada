document.addEventListener("DOMContentLoaded", function () {
    const fields = [
        { key: "name", label: "Name" },
        { key: "brand_name", label: "Brand" },
        { key: "ingredients", label: "Ingredients" },
        { key: "nutrients_energy_100g", label: "Energy (100g)" },
        { key: "nutrients_carbohydrates_100g", label: "Carbohydrates (100g)" },
        { key: "nutrients_energy_kcal_100g", label: "Energy kcal (100g)" },
        { key: "nutrients_vitamin_a_100g", label: "Vitamin A (100g)" }
    ];

    function generateTableRows() {
        let tableBody = document.getElementById("product-fields");

        fields.forEach(field => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td><strong>${field.label}</strong></td>
                <td id="off_${field.key}"></td>
                <td class="text-center">
                    <input type="checkbox" class="form-check-input copy-check" data-target="${field.key}" data-source="off_${field.key}">
                </td>
                <td><input type="text" id="result_${field.key}" class="form-control"></td>
                <td id="fdc_${field.key}"></td>
                <td class="text-center">
                    <input type="checkbox" class="form-check-input copy-check" data-target="${field.key}" data-source="fdc_${field.key}">
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    function loadProduct() {
        fetch("/api/get_product")
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("No matching product found.");
                    return;
                }

                document.getElementById("id_match").textContent = data.id_match || "";

                fields.forEach(field => {
                    document.getElementById("off_" + field.key).textContent = data["off_" + field.key] || "";
                    document.getElementById("fdc_" + field.key).textContent = data["fdc_" + field.key] || "";
                    document.getElementById("result_" + field.key).value = "";
                });

                document.querySelectorAll(".copy-check").forEach(checkbox => {
                    checkbox.checked = false;
                });
            })
            .catch(error => console.error("Error loading product:", error));
    }

    document.addEventListener("change", function (event) {
        if (event.target.classList.contains("copy-check")) {
            const target = event.target.dataset.target;
            const source = event.target.dataset.source;
            document.getElementById("result_" + target).value = document.getElementById(source).textContent;
        }
    });

    document.getElementById("mergeBtn").addEventListener("click", function () {
        let mergedProduct = { id_match: document.getElementById("id_match").textContent };

        fields.forEach(field => {
            mergedProduct[field.key] = document.getElementById("result_" + field.key).value;
        });

        fetch("/api/merge", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mergedProduct)
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadProduct();
            })
            .catch(error => console.error("Error merging product:", error));
    });

    generateTableRows();
    loadProduct();
});