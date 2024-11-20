
function callFunction() {
    const button = document.getElementById("analyze");
    button.disabled = true;
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            const array_data = data;
            update = update_render(data);
            button.disabled = false;
        });
}