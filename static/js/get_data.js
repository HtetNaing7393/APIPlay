
function callFunction() {
    const button = document.getElementById("analyze");
    button.disabled = true;
    fetch("/button-click", {
        method: "POST"
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById("result").innerText = data;
            button.disabled = false;
        });
}