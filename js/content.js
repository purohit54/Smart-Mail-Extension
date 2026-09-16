function extractEmail() {
    try {
            // Gmail currently opened email
    const email = document.querySelector('div[role="main"]');

    if (!email) {
        console.log("No email opened");
        return;
    }

    // Sender
    const senderElement = email.querySelector(
        'span[email]'
    );

    const from = senderElement
        ? senderElement.getAttribute("email")
        : null;

    // Subject
    const subjectElement = email.querySelector("h2");

    const subject = subjectElement
        ? subjectElement.innerText.trim()
        : null;

    // Date
    const dateElement = email.querySelector(
        'span[title]'
    );

    const date = dateElement
        ? dateElement.getAttribute("title")
        : null;

    // Body
    const bodyElement = email.querySelector(
        'div[role="main"] div.a3s'
    );

    const body = bodyElement
        ? bodyElement.innerText.trim()
        : null;

    const emailData = {
        from: from,
        subject: subject,
        date: date,
        body: body
    };

    console.log("Email data:", emailData);

    chrome.runtime.sendMessage({
        type: "EMAIL_DATA",
        data: emailData
    });
    } catch (error) {
        if (error.message.includes("Extension context invalidated")) {
            console.log("Extension was reloaded. Stopping content script.");
            return;
            }
    }

}


const observer = new MutationObserver(() => {
    try {
        clearTimeout(timer);
        
        timer = setTimeout(() => {
                getCurrentMail();
            }, 400);
        
        extractEmail();
    } catch (error) {
        if (error.message.includes("Extension context invalidated")) {
            observer.disconnect();
            return;
        }

        console.error(error);
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
