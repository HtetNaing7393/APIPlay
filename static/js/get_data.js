
function callFunction() {
    const button = document.getElementById("analyze");
    button.disabled = true;
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            const array_data = data;
            const overall_info = array_data[0]
            const api_info = array_data[1]
            const endpoint_info = array_data[2]
            document.getElementById("num_apis").innerText = overall_info["apis"]
            document.getElementById("num_specs").innerText = overall_info["specifications"]
            document.getElementById("num_endpoints").innerText = overall_info["endpoints"]
            document.getElementById("num_api_versions").innerText = api_info["total"]
            document.getElementById("num_endpoint_versions").innerText = endpoint_info["total"]
            update = update_render(array_data[0]);
            document.getElementById("num_apis").innerText = array_data[1];
            total = array_data[0].reduce((one, two) => one + two)
            document.getElementById("num_endpoints").innerText = total;
            button.disabled = false;
        });
}