
function callFunction() {
    const button = document.getElementById("analyze");
    button.disabled = true;
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            const array_data = data;
            update = update_render(array_data[0]);
            document.getElementById("num_apis").innerText = array_data[1];
            total = array_data[0].reduce((one, two) => one + two)
            document.getElementById("num_endpoints").innerText = total;
            button.disabled = false;
        });
}