/**
 * flashcards.js — Converts <details> inside .flashcard-deck into flip cards.
 *
 * Markdown usage:
 *   <div class="flashcard-deck" markdown>
 *   
 *   <details class="flashcard" markdown>
 *   <summary>Question text here</summary>
 *   Answer content here (supports **bold**, tables, lists, blockquotes)
 *   </details>
 *   
 *   </div>
 */
document.addEventListener("DOMContentLoaded", function () {
    // Wait a tick for MkDocs to finish rendering
    setTimeout(transformFlashcards, 100);
});

// Also handle MkDocs instant navigation
if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
        setTimeout(transformFlashcards, 100);
    });
}

function transformFlashcards() {
    document.querySelectorAll(".flashcard-deck details.flashcard").forEach(function (detail, idx) {
        // Skip already transformed
        if (detail.dataset.transformed) return;
        detail.dataset.transformed = "true";

        var summary = detail.querySelector("summary");
        var question = summary ? summary.innerHTML : "";

        // Get answer content (everything after summary)
        var answerParts = [];
        var children = detail.childNodes;
        var pastSummary = false;
        for (var i = 0; i < children.length; i++) {
            if (children[i] === summary) {
                pastSummary = true;
                continue;
            }
            if (pastSummary) {
                if (children[i].outerHTML) {
                    answerParts.push(children[i].outerHTML);
                } else if (children[i].textContent && children[i].textContent.trim()) {
                    answerParts.push("<p>" + children[i].textContent + "</p>");
                }
            }
        }
        var answer = answerParts.join("");

        // Build flip card
        var card = document.createElement("div");
        card.className = "flashcard";
        card.innerHTML =
            '<div class="flashcard-inner">' +
            '<div class="flashcard-front">' +
            '<span class="card-num">' + (idx + 1) + "</span>" +
            "<p>" + question.replace(/^❓\s*/, "") + "</p>" +
            "</div>" +
            '<div class="flashcard-back">' +
            answer +
            "</div>" +
            "</div>";

        card.addEventListener("click", function () {
            card.classList.toggle("flipped");
        });

        detail.parentNode.replaceChild(card, detail);
    });
}
