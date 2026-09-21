const API_URL = window.location.origin;


const pdfInput = document.getElementById("pdfInput");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");
const fileName = document.getElementById("fileName");

const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");

const loading = document.getElementById("loading");
const answerSection = document.getElementById("answerSection");
const answer = document.getElementById("answer");
const sources = document.getElementById("sources");


pdfInput.addEventListener("change", () => {

    if (pdfInput.files.length > 0) {

        const file = pdfInput.files[0];

        fileName.textContent =
            `Selected: ${file.name}`;
    }
});


uploadBtn.addEventListener("click", async () => {

    if (!pdfInput.files.length) {

        uploadStatus.textContent =
            "Please select a PDF first.";

        return;
    }

    const file = pdfInput.files[0];

    if (!file.name.toLowerCase().endsWith(".pdf")) {

        uploadStatus.textContent =
            "Only PDF files are supported.";

        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    uploadBtn.disabled = true;

    uploadStatus.textContent =
        "Uploading and indexing...";

    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Upload failed"
            );
        }

        uploadStatus.textContent =
            `${data.message} (${data.chunks} chunks)`;

    } catch (error) {

        uploadStatus.textContent =
            `Error: ${error.message}`;

    } finally {

        uploadBtn.disabled = false;
    }
});


askBtn.addEventListener("click", async () => {

    const question =
        questionInput.value.trim();

    if (!question) {

        alert("Please enter a question.");

        return;
    }

    askBtn.disabled = true;

    loading.classList.remove("hidden");

    answerSection.classList.add("hidden");

    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Request failed"
            );
        }

        answer.textContent = data.answer;

        sources.innerHTML = "";

        data.sources.forEach(source => {

            const sourceElement =
                document.createElement("div");

            sourceElement.className = "source";

            const title =
                document.createElement("strong");

            title.textContent =
                `📄 ${source.filename} · Page ${source.page}`;

            const text =
                document.createElement("div");

            text.className = "source-text";

            text.textContent = source.text;

            sourceElement.appendChild(title);
            sourceElement.appendChild(text);

            sources.appendChild(sourceElement);
        });

        answerSection.classList.remove("hidden");

    } catch (error) {

        answer.textContent =
            `Error: ${error.message}`;

        answerSection.classList.remove("hidden");

    } finally {

        askBtn.disabled = false;

        loading.classList.add("hidden");
    }
});