chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (message.type === "EMAIL_DATA") {

            console.log("Email received from content.js:");

            // console.log("From:", message.data.from);
            // console.log("Subject:", message.data.subject);
            // console.log("Date:", message.data.date);
            // console.log("Body:", message.data.body);

            // This is where you can send the data
            // to your Python/FastAPI backend.
            console.log("About to call FastAPI");
            fetch("http://127.0.0.1:8000/email", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(message.data)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Backend response:", data);
            })
            .catch(error => {
                console.error("Backend error:", error);
            });
        }
    }
);
