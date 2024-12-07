
// Function to handle the button click event
function callFunction() {
    // Disable the analyze button to prevent multiple clicks
    const button = document.getElementById("analyze");
    button.disabled = true;

    // Send a POST request to the server
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            // Extract data from the response
            const array_data = data;
            const overall_info = array_data[0];
            const api_info = array_data[1];

            // Convert API info object to an array
            let api_array = Object.values(api_info);
            // Get API version formats and methods
            let api_v_formats = get_v_formats(api_array);
            let api_v_methods = get_v_methods(api_array);

            const endpoint_info = array_data[2];
            // Convert endpoint info object to an array
            let endpoint_array = Object.values(endpoint_info);
            // Get endpoint version formats and methods
            let endpoint_v_formats = get_v_formats(endpoint_array);
            let endpoint_v_methods = get_v_methods(endpoint_array);

            // Update the DOM elements with the extracted information
            document.getElementById("num_apis").innerText = overall_info["apis"];
            document.getElementById("num_specs").innerText = overall_info["specifications"];
            document.getElementById("num_endpoints").innerText = overall_info["endpoints"];
            document.getElementById("num_api_versions").innerText = api_info["total"];
            document.getElementById("num_endpoint_versions").innerText = endpoint_info["total"];

            // Call the update_render function with the extracted formats and methods
            update = update_render(api_v_formats, api_v_methods, endpoint_v_formats, endpoint_v_methods);

            // Re-enable the analyze button
            button.disabled = false;
        });
}

// Function to get version formats from an array
function get_v_formats(array) {
    let result = [];
    // Extract the first 6 elements
    for (let i = 0; i < 6; i++) {
        result.push(array[i]);
    }
    return result;
}

// Function to get version methods from an array
function get_v_methods(array) {
    let result = [];
    // Extract elements from index 6 to 7
    for (let i = 6; i < 8; i++) {
        result.push(array[i]);
    }
    return result;
}