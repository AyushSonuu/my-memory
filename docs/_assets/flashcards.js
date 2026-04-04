/**
 * flashcards.js — Converts <details class="flashcard"> inside .flashcard-deck into flip cards.
 * Uses show/hide toggle so ALL content is always visible — no text clipping.
 */
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(transformFlashcards, 100);
});

// Handle MkDocs instant navigation
if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
        setTimeout(transformFlashcards, 100);
    });
}

function transformFlashcards() {
    document.querySelectorAll(".flashcard-deck details.flashcard").forEach(function (detail, idx) {
        if (detail.dataset.transformed) return;
        detail.dataset.transformed = "true";

        var summary = detail.querySelector("summary");
        var question = summary ? summary.innerHTML.replace(/^❓\s*/, "") : "";

        // Collect answer content
        var answerParts = [];
        var children = detail.childNodes;
        var pastSummary = false;
        for (var i = 0; i < children.length; i++) {
            if (children[i] === summary) { pastSummary = true; continue; }
            if (pastSummary) {
                if (children[i].outerHTML) answerParts.push(children[i].outerHTML);
                else if (children[i].textContent && children[i].textContent.trim())
                    answerParts.push("<p>" + children[i].textContent + "</p>");
            }
        }

        var card = document.createElement("div");
        card.className = "flashcard";
        card.innerHTML =
            '<div class="flashcard-inner">' +
                '<div class="flashcard-front">' +
                    '<span class="card-num">' + (idx + 1) + '</span>' +
                    '<p>' + question + '</p>' +
                '</div>' +
                '<div class="flashcard-back">' +
                    answerParts.join("") +
                '</div>' +
            '</div>';

        card.addEventListener("click", function () {
            card.classList.toggle("flipped");
        });

        detail.parentNode.replaceChild(card, detail);
    });
}
