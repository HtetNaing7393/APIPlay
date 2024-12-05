
function callFunction() {
    const button = document.getElementById("analyze");
    button.disabled = true;
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            const array_data = data;
            const overall_info = array_data[0];
            const api_info = array_data[1];
            let api_array = Object.values(api_info);
            let api_v_formats = get_v_formats(api_array);
            let api_v_methods = get_v_methods(api_array);
            const endpoint_info = array_data[2];
            let endpoint_array = Object.values(endpoint_info);
            let endpoint_v_formats = get_v_formats(endpoint_array);
            let endpoint_v_methods = get_v_methods(endpoint_array);

            document.getElementById("num_apis").innerText = overall_info["apis"]
            document.getElementById("num_specs").innerText = overall_info["specifications"]
            document.getElementById("num_endpoints").innerText = overall_info["endpoints"]
            document.getElementById("num_api_versions").innerText = api_info["total"]
            document.getElementById("num_endpoint_versions").innerText = endpoint_info["total"]

            document.getElementById("test").innerText = api_v_methods;

            update = update_render(api_v_formats, api_v_methods, endpoint_v_formats, endpoint_v_methods);

            button.disabled = false;
        });
}

function get_v_formats(array) {
    let result = [];
    for (let i = 0; i < 5; i++) {
        result.push(array[i])
    }
    return result;
}

function get_v_methods(array) {
    let result = [];
    for (let i = 6; i < 8; i++) {
        result.push(array[i])
    }
    return result;
}