async function getNews() {
    const container = document.getElementById("newsList");
    const lang = document.getElementById("language").value;

    // ✅ SHOW LOADING
    container.innerHTML = `
        <div style="text-align:center; font-size:18px;">
            ⏳ Fetching latest news...
        </div>
    `;

    // Allow UI to render
    await new Promise(resolve => setTimeout(resolve, 500));

    try {
        const res = await fetch("/get_news", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ language: lang })
        });

        const news = await res.json();

        console.log("FRONTEND NEWS:", news);

        // ❌ If empty
        if (!news || news.length === 0) {
            container.innerHTML = `
                <div style="text-align:center; color:red;">
                    ⚠️ No news available
                </div>
            `;
            return;
        }

        container.innerHTML = "";

        news.forEach(item => {
            const card = document.createElement("div");
            card.className = "card";

            const title = item.title || "No title available";
            const full = item.full || title;

            card.innerHTML = `
                <h3>${title}</h3>
                <button class="play-btn"
                    onclick="playNews('${encodeURIComponent(full)}', this)">
                    🔊 Play
                </button>
            `;

            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        container.innerHTML = `
            <div style="color:red; text-align:center;">
                ❌ Failed to load news
            </div>
        `;
    }
}


async function playNews(encodedText, btn) {
    try {
        const text = decodeURIComponent(encodedText);

        btn.innerText = "⏳ Loading...";

        const res = await fetch("/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        console.log("AUDIO RESPONSE:", data);

        // ❌ ERROR HANDLING
        if (!data.audio) {
            alert("Something went wrong with audio");
            btn.innerText = "🔊 Play";
            return;
        }

        const audio = new Audio(data.audio);

        audio.play()
            .then(() => {
                btn.innerText = "⏸ Playing...";
            })
            .catch(err => {
                console.error("Audio play error:", err);
                alert("Audio playback failed");
                btn.innerText = "🔊 Play";
            });

        audio.onended = () => {
            btn.innerText = "🔊 Play";
        };

    } catch (err) {
        console.error(err);
        alert("Something went wrong");
        btn.innerText = "🔊 Play";
    }
}