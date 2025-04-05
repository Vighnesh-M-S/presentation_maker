async function processText() {
    let text = document.getElementById("textInput").value;

    let response = await fetch("http://127.0.0.1:9090/processText/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: text })
});
let result = await response.json();
document.getElementById("output").textContent = JSON.stringify(result, null, 2);
}