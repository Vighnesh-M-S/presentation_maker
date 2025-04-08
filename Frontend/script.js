async function processText() {
    let text = document.getElementById("textInput").value;

    // Show loading message
    const output = document.getElementById("output");
    output.innerHTML = "<em>Creating slides…</em>";

    try {
        const response = await fetch("http://127.0.0.1:9090/processText/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: text })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.statusText);
        }

        const result = await response.json();

        // Format result with clickable link
        output.innerHTML = `
            <strong>📥 Query Received:</strong><br>
            <a href="${result.query_received}" target="_blank">${result.query_received}</a><br><br>
            <strong>📤 Slide Link:</strong><br>
            <a href="${result.response}" target="_blank">${result.response}</a>
        `;
    } catch (error) {
        output.innerHTML = `<span style="color:red;">❌ Error: ${error.message}</span>`;
    }
}
