const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");

tableOutput.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value.trim();

    if (searchValue.length > 0) {
        paginationContainer.style.display = "none";
        fetch("/search-expenses/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.length === 0) {
                console.log("No data");
                appTable.style.display = "none";
                tableOutput.style.display = "block";
                tableBody.innerHTML = "<tr><td colspan='4'>No results found</td></tr>";
            } else {
                appTable.style.display = "none";
                tableOutput.style.display = "block";
                let tableRows = "";
                data.forEach((item) => {
                    tableRows += `
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.date}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>
                                <a href="{% url 'edit-expense' expense.id %}" class="btn btn-primary btn-sm">Edit</a>
                                <a href="{% url 'delete-expense' expense.id   %}" class="btn btn-danger btn-sm">Delete</a>
                            </td>
                        </tr>
                    `;
                });
                tableBody.innerHTML = tableRows;
            }
        })
        .catch((error) => {
            console.error("Error fetching search results:", error);
            // Handle error
        });
    } else {
        appTable.style.display = "block";
        tableOutput.style.display = "none";
        paginationContainer.style.display = "block";
    }
});
