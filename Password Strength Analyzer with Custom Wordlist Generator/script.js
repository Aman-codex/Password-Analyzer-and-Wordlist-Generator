// =============================
// Password Analyzer & Wordlist Generator
// =============================

// Elements
const passwordInput = document.getElementById("passwordInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const analysisResult = document.getElementById("analysisResult");

const hintsInput = document.getElementById("hintsInput");
const generateBtn = document.getElementById("generateBtn");
const wordlistResult = document.getElementById("wordlistResult");
const downloadBtn = document.getElementById("downloadBtn");

// =============================
// Password Strength Analyzer
// =============================
function analyzePassword(password) {
    let score = 0;
    let feedback = [];

    // Length check
    if (password.length >= 12) {
        score += 2;
    } else if (password.length >= 8) {
        score += 1;
    } else {
        feedback.push("Too short (use at least 8 characters).");
    }

    // Character variety
    if (/[a-z]/.test(password)) score++;
    else feedback.push("Add lowercase letters.");

    if (/[A-Z]/.test(password)) score++;
    else feedback.push("Add uppercase letters.");

    if (/[0-9]/.test(password)) score++;
    else feedback.push("Add numbers.");

    if (/[^a-zA-Z0-9]/.test(password)) score++;
    else feedback.push("Add special characters (!@#$ etc.).");

    // Overall strength
    let strength = "Weak";
    if (score >= 6) strength = "Very Strong";
    else if (score >= 4) strength = "Strong";
    else if (score >= 3) strength = "Moderate";

    return { strength, feedback };
}

analyzeBtn.addEventListener("click", () => {
    const password = passwordInput.value.trim();
    if (!password) {
        analysisResult.innerHTML = `<p class="text-red-500">⚠️ Please enter a password.</p>`;
        return;
    }

    const { strength, feedback } = analyzePassword(password);

    let feedbackHtml = "";
    if (feedback.length > 0) {
        feedbackHtml = `<ul class="list-disc list-inside text-sm text-red-600">
            ${feedback.map(f => `<li>${f}</li>`).join("")}
        </ul>`;
    }

    analysisResult.innerHTML = `
        <p class="font-bold">Strength: <span class="text-blue-600">${strength}</span></p>
        ${feedbackHtml}
    `;
});

// =============================
// Wordlist Generator
// =============================
function generateWordlist(hints) {
    let words = [];

    hints.forEach(hint => {
        hint = hint.trim();
        if (!hint) return;

        // Basic variations
        words.push(hint);
        words.push(hint.toLowerCase());
        words.push(hint.toUpperCase());
        words.push(hint.charAt(0).toUpperCase() + hint.slice(1));

        // Add numbers/special chars
        [123, 2024, 99].forEach(num => words.push(hint + num));
        ["!", "@", "#"].forEach(sym => words.push(hint + sym));

        // Leetspeak replacements
        words.push(hint.replace(/a/gi, "4"));
        words.push(hint.replace(/e/gi, "3"));
        words.push(hint.replace(/i/gi, "1"));
        words.push(hint.replace(/o/gi, "0"));
    });

    // Remove duplicates
    return [...new Set(words)];
}

generateBtn.addEventListener("click", () => {
    const hints = hintsInput.value
        .split(",")
        .map(h => h.trim())
        .filter(h => h.length > 0);

    if (hints.length === 0) {
        wordlistResult.innerHTML = `<p class="text-red-500">⚠️ Please enter at least one hint.</p>`;
        downloadBtn.classList.add("hidden");
        return;
    }

    const wordlist = generateWordlist(hints);

    wordlistResult.innerHTML = `
        <p class="font-bold">Generated ${wordlist.length} words:</p>
        <textarea class="w-full h-40 border rounded p-2 mt-2 text-sm">${wordlist.join("\n")}</textarea>
    `;

    // Enable download button
    downloadBtn.classList.remove("hidden");

    // Store list in button for download
    downloadBtn.dataset.wordlist = wordlist.join("\n");
});

// =============================
// Download Wordlist
// =============================
downloadBtn.addEventListener("click", () => {
    const content = downloadBtn.dataset.wordlist;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "wordlist.txt";
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});
